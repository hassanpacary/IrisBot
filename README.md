<div style="text-align: center;">
    <h1>IrisBot</h1>
</div>

![Static Badge](https://img.shields.io/badge/Python%20version-3.13.0-blue)
![GitHub License](https://img.shields.io/github/license/hassanpacary/IrisBot)

## Introduction
IrisBot is a bot developed for the WBZ Discord server, and is the mascot of our friends circle. Its code is open source, and you can use it for your own bot if you wish!\
If you want you can also add Iris on your server from here - [Discord Discovery App](https://discord.com/discovery/applications/1332386596175220878)

[![Discord](https://discord.com/api/guilds/594579103806390313/embed.png)](https://discord.gg/Bfd2rnJkuA)

## How to use
1. Download code lastest version ;
2. Add a `.env` (dotenv) *- more info below -* ;
3. Change values in the `config.json` file ;
4. Run `pip install -r requirements.txt` in your console, from the root of the project ;
5. Execute `main.py`

## Template for the `.env file`

```
# --- DISCORD ---
# Without, not bot
DISCORD_TOKEN= [YOUR BOT TOKEN]

# --- REDDIT ---
# Without, no reddit post images
REDDIT_CLIENT_ID=[YOUR REDDIT APP ID]
REDDIT_CLIENT_SECRET=[YOUR REDDIT AP ID SECRET]
REDDIT_USER_AGENT=[YOUR USER AGENT, like this - 'discord:botname:1.0 (by u/username)']

# --- AZURE ---
# without, no Text To Speech
# You should also configure an Azure resource for it to work.
# If you have any further questions, please feel free to contact me directly !
AZURE_ENDPOINT=[AZURE RESSOURCE ENDPOINT]
AZURE_KEY=[AZURE RESSOURCE KEY]
```