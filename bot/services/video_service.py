"""
bot/services/video_service.py
© by hassanpacary

Utility functions for video downloader, mux and compression.
"""

# --- Imports ---
import asyncio
import os
import subprocess
import tempfile
from pathlib import Path

# --- Third party imports ---
import discord

# --- Bot modules ---
from bot.utils.aiohttp_client import aiohttp_client
from bot.utils.discord_utils import create_discord_file
from bot.utils.files_utils import load_file, write_file


# ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗     ██╗   ██╗██╗██████╗ ███████╗ ██████╗
# ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗    ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
# ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║    ██║   ██║██║██║  ██║█████╗  ██║   ██║
# ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║    ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
# ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝     ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
# ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝       ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝


async def download_video_and_audio_source(url: str, tmpdir: str, filename: str) -> tuple[str, str | None]:
    """
    Downloads the Reddit video and optional audio to temporary files

    Parameters:
        url (str): URL of the Reddit video
        tmpdir (str): Path to a temporary directory for intermediate files
        filename (str): Base filename to use for saved files

    Returns:
        tuple[str, str | None]: Paths to the downloaded video and audio files
                                Audio path is None if no audio is found
    """
    tmp_video_path = os.path.join(tmpdir, filename + "_video.mp4")
    tmp_audio_path = os.path.join(tmpdir, filename + "_audio.mp4")

    video_data = await aiohttp_client.download_bytes(url)
    write_file(tmp_video_path, video_data)

    audio_data = await aiohttp_client.download_bytes(url.split("DASH_")[0] + "DASH_AUDIO_128.mp4")

    # --- Audio exist ---
    if audio_data:
        write_file(tmp_audio_path, audio_data)
    else:
        tmp_audio_path = None

    return tmp_video_path, tmp_audio_path


async def merge_video_audio_in_one_file(
        video_path: str,
        audio_path: str | None,
        output_path: str):
    """
    Merges video and optional audio into a single .mp4 file using FFmpeg

    Parameters:
        video_path (str): Path to the video file
        audio_path (str | None): Path to the audio file, or None if no audio
        output_path (str): Path for the merged output file
    """
    merge_cmd = ["ffmpeg", "-y", "-i", video_path]

    if audio_path:
        merge_cmd += [
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0"
        ]
    else:
        merge_cmd += ["-c:v", "copy"]

    merge_cmd.append(output_path)

    process = await asyncio.create_subprocess_exec(
        *merge_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f'FFmpeg merge error: {stderr.decode()}')


#  ██████╗ ██████╗ ███╗   ███╗██████╗ ██████╗ ███████╗███████╗███████╗    ██╗   ██╗██╗██████╗ ███████╗ ██████╗
# ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝    ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
# ██║     ██║   ██║██╔████╔██║██████╔╝██████╔╝█████╗  ███████╗███████╗    ██║   ██║██║██║  ██║█████╗  ██║   ██║
# ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██╗██╔══╝  ╚════██║╚════██║    ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
# ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║███████╗███████║███████║     ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
#  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝      ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝


def get_video_duration(video_path: str) -> float:
    """
    Retrieves the duration of a video file using ffprobe

    Parameters:
        video_path (str): Path to the video file

    Returns:
        float: Video duration in seconds
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ],
        capture_output=True, text=True, check=True
    )

    try:
        return float(result.stdout.strip())

    except ValueError as e:
        raise RuntimeError(f"Failed to parse video duration: {result.stdout}") from e


async def compress_video(
        input_path: str,
        output_path: str,
        filesize_limit: int):
    """
    Compresses a video using FFmpeg to a target bitrate and scales to 1280px width

    Parameters:
        input_path (str): Path to the input video
        output_path (str): Path for the compressed output
        filesize_limit (int): Guild filesize limit
    """
    # Calcul the target video bitrate
    duration = get_video_duration(video_path=input_path)
    audio_bitrate_bps = 128_000
    target_total_bitrate_bps = int((filesize_limit * 8) / duration)
    target_video_bitrate_bps = max(10_000, target_total_bitrate_bps - audio_bitrate_bps)

    compress_cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-b:v", str(int(target_video_bitrate_bps)),
        "-preset", "fast",
        "-vf", "scale=1280:-2",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path
    ]

    compress_process = await asyncio.create_subprocess_exec(
        *compress_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, compress_stderr = await compress_process.communicate()

    if compress_process.returncode != 0:
        raise RuntimeError(f'FFmpeg compress error: {compress_stderr.decode()}')


# ███████╗██╗███╗   ██╗ █████╗ ██╗         ██╗   ██╗██╗██████╗ ███████╗ ██████╗
# ██╔════╝██║████╗  ██║██╔══██╗██║         ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
# █████╗  ██║██╔██╗ ██║███████║██║         ██║   ██║██║██║  ██║█████╗  ██║   ██║
# ██╔══╝  ██║██║╚██╗██║██╔══██║██║         ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
# ██║     ██║██║ ╚████║██║  ██║███████╗     ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
# ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝      ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝


async def get_video(
        url: str,
        filename: str,
        file_size_limit: int) -> discord.File | None:
    """
    Downloads, merges, and compresses a Reddit video to fit under a file size limit

    Parameters:
        url (str): URL of the Reddit video
        filename (str): Base filename without extension
        file_size_limit (int): Maximum allowed file size in bytes

    Returns:
        discord.File | None: Discord file object with the merged/compressed video
                             or None if something fails
    """
    filename_without_ext = Path(filename).stem

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_out_path = os.path.join(tmpdir, filename_without_ext + "_merged.mp4")

        video_path, audio_path = await download_video_and_audio_source(
            url=url,
            tmpdir=tmpdir,
            filename=filename
        )

        await merge_video_audio_in_one_file(
            video_path=video_path,
            audio_path=audio_path,
            output_path=tmp_out_path
        )

        # --- Return video if under filesize limit ---
        if os.path.getsize(tmp_out_path) <= file_size_limit:
            video = load_file(file_path=tmp_out_path, mode="rb")
            return create_discord_file(data=video, filename=filename)

        # --- Otherwise compress video ---
        tmp_compressed_path = os.path.join(tmpdir, filename_without_ext + "_compressed.mp4")

        await compress_video(
            input_path=tmp_out_path,
            output_path=tmp_compressed_path,
            filesize_limit=file_size_limit
        )

        compressed_video = load_file(file_path=tmp_compressed_path, mode="rb")
        return create_discord_file(data=compressed_video, filename=filename)
