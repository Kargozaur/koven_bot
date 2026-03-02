# Koven-Bot

## Description

Koven bot is a discord bot for the Koven guild in WoW. Currently supports only RaiderIO API

## Features

- [x] Liveness status

- [x] Character Management
  - [x] Create a character
  - [x] Set character inactive
  - [x] Automatic [polling](src.cogs.rio_cog.py) on startup and once every 30 minutes

## Installation

1. Clone the repository: `git clone https://github.com/Kargozaur/koven_bot`
2. Navigate to the directory: `cd koven_bot`
2. Install the dependencies: `uv sync --frozen`
3. Create a `.env` file in the root directory and add tokens:

```RIO_KEY= <your key>
DISCORD_TOKEN=<discord_token>
BNET_SECRET=<your bnet secret>
BNET_ID=<your bnet id>
```
4. Create .db.env file if you want to run it using postgres:

```
DB_TYPE=postgres
DB_USER=postgres
DB_PASSWORD=1234
DB_DRIVER=asyncpg
DB_HOST=localhost
DB_NAME=rio
DB_PORT=5433
```

## Usage
To run the project:
`uv run -m src.main` if you're using uv or `python3 -m src.main`
If you're starting it on Windows, 3 may be omitted if using python command directly