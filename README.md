<div style="text-align: center;">
    <h1>IrisBot</h1>
</div>

![Static Badge](https://img.shields.io/badge/bot_version-1.0.0-red)
![Static Badge](https://img.shields.io/badge/python%20version-3.13.13-blue)
![Discord.py](https://img.shields.io/badge/discord.py-2.7.1-5865F2)
![GitHub License](https://img.shields.io/github/license/hassanpacary/IrisBot)
![Black](https://img.shields.io/badge/code%20style-black-000000)
![isort](https://img.shields.io/badge/imports-isort-1674b1)
![Pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)

## I. Introduction

IrisBot is a bot developed for the WBZ Discord server, and is the mascot of our friends circle. Code is open source, you
can use it if you wish!

## II. How to install

1. Download code lastest version ;
2. Fill the `.env.template` (dotenv) file and rename it `.env` ;
3. Change values on all config files as you wish ;
    - `bot/cogs/[cog name]/[cog name]_config` for commands name, description and configuration constantes **(you can DEACTIVATE cog by setting ACTIVE in FALSE in this file)**.
    - `bot/cogs/[cog name]/[cog name]_strings` for responses strings.
    - `bot/config` for other constantes config data (like assets path, colors or regex)
4. Init your py venv ;
5. Run `pip install -e ".[dependencies]"` in your console, from the root of the project ;
6. Execute `main.py`

## III. Reddit Cog using ffmpeg

Reddit cog depend on [ffmpeg](https://ffmpeg.org/). Install it and configure it in your system environment variables.

## IV. Style guideline and Dev tools

This project follows
the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

**Three tools are used to enforce code quality and consistency :**

- **[Black](https://black.readthedocs.io/)** — automatic code formatter, ensures a consistent style across the codebase
- **[isort](https://pycqa.github.io/isort/)** — automatically sorts and groups imports following the Black style
  profile
- **[Pylint](https://pylint.readthedocs.io/)** — static code analysis, enforces style rules and catches potential errors

### Setup

Install dev tools dependencies from the root of the project :

```bash
pip install -e ".[dev]"
```

Run the tools manually :

```bash
black .       # format all files
isort .       # sort all imports
pylint bot/   # analyse code quality
```

## V. Version guide

Versions follow the `x.y.z` format. You can find the current version of the bot in the `pyproject.toml` file.

- **x** — major version, breaking changes or full rework
- **y** — new feature added
- **z** — bug fix or patch

## VI. Commit guideline

### Structure

```
<type>: <50 char max summary>

<75 char max description or list>
```

### Types

- **feat**
- **fix**
- **chore**
- **docs**
- **refactor**
