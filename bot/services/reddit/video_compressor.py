"""Video compressor service for reddit cog.

Manage logics functions for download video, mux, and compression.
Downloads video and audio streams separately, merges them with FFmpeg,
then compresses the result if it exceeds the Discord filesize limit for the guild.

© by hassanpacary
"""

# --- Standard library ---
import asyncio
import io
import logging
import os
import tempfile
from pathlib import Path

# --- Third-party ---
import aiohttp
import discord

# --- Internal ---
from bot.utils import files_utils, strings_utils


# --- Run ffprobe ---


async def _run_ffprobe(*args: str) -> str:
    """Runs a ffprobe command asynchronously and returns stdout.

    ffprobe is FFmpeg's inspection tool,
    which is used to read information from a media file.

    Args:
        *args: ffprobe arguments.

    Returns:
        The stdout output as a string.

    Raises:
        RuntimeError: If ffprobe exits with a non-zero return code.
    """
    process = await asyncio.create_subprocess_exec(
        "ffprobe",
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Retrieve ffprobe process data (stdout) and errors (stderr)
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"ffprobe error: {stderr.decode()}")

    return stdout.decode()


# --- Download video ---


async def _download_video_and_audio(
    url: str,
    tmpdir: str,
    filename: str,
) -> tuple[str, str | None]:
    """Downloads Reddit video and audio to temporary files.

    Reddit stores video and audio as separate DASH streams. The audio
    URL is derived from the video URL by replacing the quality segment.

    Args:
        url: URL of the Reddit video stream.
        tmpdir: Path to a temporary directory for intermediate files.
        filename: Base filename (without extension) for saved files.

    Returns:
        A tuple of (video_path, audio_path). audio_path is None if
        no valid audio stream is found.
    """
    video_path = os.path.join(tmpdir, filename + "_video.mp4")
    audio_path = os.path.join(tmpdir, filename + "_audio.mp4")

    # Download video bytes for manipulate its.
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url=url)
            video_bytes = await resp.read()
    except aiohttp.ClientError as e:
        logging.error("Failed to download video %s: %s", url, e)

    await files_utils.write_file(fp=video_path, data=video_bytes)

    # The Reddit audio streams url.
    audio_url = url.split("CMAF_")[0] + "CMAF_AUDIO_128.mp4"

    # Audio is in a distinct file because Reddit store it in a separate streams.
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url=audio_url)
            audio_bytes = await resp.read()
    except aiohttp.ClientError as e:
        logging.error("Failed to download audio %s: %s", audio_url, e)

    # Return video and audio streams files.
    if audio_bytes:
        await files_utils.write_file(fp=audio_path, data=audio_bytes)
        return video_path, audio_path

    # Return only video streams file, no audio found.
    return video_path, None


# --- Merge video and audio streams ---


async def _merge_video_audio(
    video_path: str,
    audio_path: str | None,
    tmpdir: str,
    filename: str,
) -> str:
    """Merges video and audio streams into a single MP4 file using FFmpeg.

    Merging command ffmpeg args:
        - "ffmpeg": FFMPEG executable.
        - "-y": Suppress the output file.
        - "-i video_path": Video_path is declared at the source file (index 0).
        - "-i audio_path": Audio_path is declared at the source file (index 1).
        - "-c:v copy": paste video flux
        - "- c:a aac": re encode the audio flux in AAC. Because we need to make sure
        the audio format is standardized.
        - "-map 0:v:0": Explicite mapping of video flux index 0.
        - "-map 0:a:0": Explicite mapping of audio flux index 1.
        - "-movflags +faststart": Moves the MP4 metadata to the start of the file,
        so Discord can start streaming before the full file is downloaded.
        - merged_path": Path of the result file (output).

    Args:
        video_path: Path to the video file.
        audio_path: Path to the audio file, or None if no audio.
        tmpdir: Path to a temporary directory for intermediate files.
        filename: Base filename (without extension) for saved files.

    Raises:
        RuntimeError: If FFmpeg exits with a non-zero return code.
    """
    merged_path = os.path.join(tmpdir, filename + "_merged.mp4")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-movflags", "+faststart",
        merged_path,
    ]

    # Get all the command's arguments and retrieve result
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Retrieve only the possibles errors.
    _, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg merge error: {stderr.decode()}")

    return merged_path


async def _has_audio_stream(
        video_path: str,
        audio_path: str | None,
        tmpdir: str,
        filename: str
) -> str:
    """Checks if audio file contains an audio stream.

    If the audio_path exist and the file contain audio flux and/or is not corrupted,
    call _merge_video_audio for merge video and audio streams in the same file.
    If not, return the video flux

    Command ffprobe args:
        - "-v error": Log level set to error for avoid false positives
        if a log contains the word "audio".
        - "-select_streams a": Listen only audio flux (type a).
        - "-show_entries stream=codec_type": extracts the value of the codec_type field
        (such as "audio" or "video," depending on the stream).
        - "-of default=noprint_wrappers=1:nokey=1": default output format but without
        tags and only the brut value of the codec_type (so "audio" or "video").
        - audio_path: the audio file to analyze.

    Args:
        video_path: Path to the video file.
        audio_path: Path to the audio file, or None if no audio.
        tmpdir: Path to a temporary directory for intermediate files.
        filename: Base filename (without extension) for saved files.

    Returns:
        True if an audio stream is detected, False otherwise.
    """
    if audio_path is not None:
        stdout = await _run_ffprobe(
            "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=codec_type",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path,
        )

        has_audio = "audio" in stdout

        if has_audio:
            return await _merge_video_audio(
                video_path=video_path,
                audio_path=audio_path,
                tmpdir=tmpdir,
                filename=filename,
            )

    return video_path


# --- Compress video ---


async def _get_video_duration(video_path: str) -> float:
    """Retrieves the duration of a video file using ffprobe.

    Command ffprobe args:
        - "-v error": Log level set to error for avoid false positives
        if a log contains the word "audio".
        - "-select_streams v:0": Listen only video flux (type v).
        - "-show_entries format=duration": extracts the value of the duration field
        - "-of default=noprint_wrappers=1:nokey=1": default output format but without
        tags and only the brut value of the duration field (in secondes).
        - video_path: the video file to analyze.

    Args:
        video_path: Path to the video file.

    Returns:
        Video duration in seconds.

    Raises:
        RuntimeError: If the duration cannot be parsed.
    """
    stdout = await _run_ffprobe(
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path,
    )

    try:
        return float(stdout.strip())
    except ValueError as e:
        raise RuntimeError(f"Failed to parse video duration: {stdout}") from e


async def _compress_video(
    input_path: str,
    tmpdir: str,
    filename: str,
    filesize_limit: int,
) -> str:
    """Compresses a video to fit within a target file size using FFmpeg.

    Computes the target bitrate from the file size limit and video
    duration, then re-encodes with libx264 scaled to 1280px width.

    Compress command ffmpeg args:
        - "ffmpeg": FFMPEG executable.
        - "-y": Suppress the output file without confirmation.
        - "-i input_path": video path is declared at the source file (index 0).
        - "-c:v libx264": H.264 codex, for compress the video.
        - "-b:v str(target_video_bps)": Bitrate cible of the video.
        - "-preset _FFMPEG_PRESET": Apply the ffmpeg encodage preset.
        - "-vf scale=slow:-2": (video filter) Rescale the video.
        - "- c:a aac": re encode the audio flux in AAC. Because we need to make sure
        the audio format is standardized.
        - "-b:a, _AUDIO_BITRATE_K": Re encode the audio à 128k.
        - compress_path: Output file.

    Args:
        input_path: Path to the input video.
        tmpdir: Path to a temporary directory for intermediate files.
        filename: Base filename (without extension) for saved files.
        filesize_limit: Maximum allowed file size in bytes.

    Raises:
        RuntimeError: If FFmpeg exits with a non-zero return code.
    """
    compressed_path = os.path.join(tmpdir, filename + "_compressed.mp4")

    video_duration = await _get_video_duration(video_path=input_path)

    # Retrieve total target bps (video and audio).
    target_total_bps = int((filesize_limit * 8) / video_duration)

    # Allow audio bitrate
    audio_bitrate_bps = min(128000, int(target_total_bps * 0.2))
    audio_bitrate_bps = max(audio_bitrate_bps, 64_000)
    audio_bitrate_k = f"{audio_bitrate_bps // 1000}k"

    # Retrieve the video target bps (without the bps allowed to the audio).
    target_video_bps = max(
        10000,
        target_total_bps - audio_bitrate_bps,
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-b:v", str(target_video_bps),
        "-preset", "slow",
        "-vf", "scale='min(1280, iw)':-2",
        "-c:a", "aac",
        "-b:a", audio_bitrate_k,
        compressed_path,
    ]

    # Get all the command's arguments and retrieve result
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Retrieve only the possibles errors.
    _, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg compress error: {stderr.decode()}")

    return compressed_path


# --- Return Reddit video ---


async def get_video(
    url: str,
    file_size_limit: int,
) -> discord.File | None:
    """Downloads, merges video and audio and compresses (if necessary)
    a Reddit video to fit Discord's limit.

    If the file size exceeds the guild's filesize limit, compresses it to fit.

    Args:
        url: URL of the Reddit video stream.
        file_size_limit: Maximum allowed file size in bytes.

    Returns:
        A discord.File ready to upload, or None if processing fails.
    """
    filename = (
        strings_utils.get_string_segment(string=url, split_char="/", i=2)
        or "video.mp4"
    )

    # Stem retrieve the filename without its extension.
    # We need the filename without its extension later,
    # so we can merge the video with its audio while keeping the original filename.
    filename_without_extension = Path(filename).stem

    # Create a temporary directory for manipulate the Reddit video and audio.
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            video_path, audio_path = await _download_video_and_audio(
                url=url,
                tmpdir=tmpdir,
                filename=filename_without_extension,
            )

            merged_path = await _has_audio_stream(
                video_path=video_path,
                audio_path=audio_path,
                tmpdir=tmpdir,
                filename=filename_without_extension,
            )

            if os.path.getsize(merged_path) <= file_size_limit:
                original_video = await files_utils.load_file(fp=merged_path)
                return discord.File(fp=io.BytesIO(original_video), filename=filename)

            compressed_path = await _compress_video(
                input_path=merged_path,
                tmpdir=tmpdir,
                filename=filename_without_extension,
                filesize_limit=file_size_limit,
            )

            compressed_video = await files_utils.load_file(fp=compressed_path)
            return discord.File(fp=io.BytesIO(compressed_video), filename=filename)
        except RuntimeError as e:
            logging.error("Failed to process video from %s: %s", url, e)
            return None
