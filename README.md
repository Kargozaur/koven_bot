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

## Extras

- [Dishka](https://dishka.readthedocs.io/en/stable/quickstart.html) for the Dependency Injection.


Dependency graph may be viewed using [d2land](https://play.d2lang.com/?script=pFW9bts8FN39FISm7xtihHb8OxRwbAPtZDeqkVFgKNohkpACySQNij5Dhz5Ap459tz5CQcmUxFCibEmLDZLnnnN5L8-VmCcEzkEQ6j_9xXYbfOsBgPlTwhlhauBs7RFWXLwN5yD4--vnb7CQbwwvOVOIMiLSI_qT9yghc4AfkZQ9AL73ACjAVyn4xx8QEqUoO8g6mP4Cc2gr-AuNiegfiIrkcfG__4M5CAKHYmQoFndSCYTV6nrJ2Z4ezqeK7yKcQgsu_ZmzDvXYUK-oxFzE7ZOMswAVyXoFTIyAG8rbkwvKzyWe5peum2LNDpQRL_Hq2qIkKcIme18_h3RmSJEmjSSRknL2hB6IiFIdYbYSnaOkHOWdniI1Rwq8tC5g-UgJU17aj0olXy3mLAucQuuaG8K8wkgDP21CIl4oJg1VTs9UFDldr0gzS-C4UmomV9DACFreI10tInZJjFS9IaSKsjOWIGzw0XMWoEqWcRujzL6EQl3pJzO6fmFsfeNF4OLiQ_32qAN23AE78WFHfuzUh536sTMfFl76wRD60JMu4GEDeODVDU9GD_OBd7P-vFuHX-x5CK8q902cUZepCMeWexxtq4Vr2U-myRZdHfn82DGqNvtbLh78z3hza8l45q8Vr_bI59JNHe9o62aFeVR6WpGOKyKfIptX1l4A1-DTyU_xp1mpdYf9UiPmzVvYTM1-Y4RJQ4RJY4Rp5wjaeHr_AgAA__8%3D&). Plotter provided by dishka.
- discord.py as discord client
