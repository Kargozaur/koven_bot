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

- [Dishka](https://dishka.readthedocs.io/en/stable/quickstart.html) for the Dependency Injection
Dependency graph may be viewed using [d2land](https://play.d2lang.com/?script=pFa7btswFN39FYSmdohhSnH8GAoktoF0qV27RkaBkWmbSEIKJPNC0W_o0A_o1LH_1k8oKJmiGUpUZGmxQfLcc-694rkSCUsxHINgpf50LxeL4HsHgIQ9pIxiKkNna4sSyfhrNAbBv9-__oBL8UqTCaMSEYp5dkQ9Yo9SPAbJPRKiA8CPDgAGfJ6Bf_4FKywloTtRBVNPoA8tOHsiG8y7OyxjcVj88DEYgyBwKPqa4vJWSI4SOb2aMLolu-ZUm9s4yaCGSz36rEN9oamnRCSMb05PcpMHKEnWK2CgBSwJO52cE9aUeFgUXb0UM7ojFHuJp1cWJc4QNtnb_jmkI02KFGkssBCE0Qd0h3mc6VjlK3ETJcdR3ugxqTlSYM8qwOSeYCq9tNdSpi8Wc55FkkGrXm4Iiw4jBfw8X2H-RBJc0-XsTEmTs_WSNPMEDitHL5MrKNSCJnukuoX5Ot0gWW0ImaL8jCUo0fj4MQ9QJku7jVZmF8GoO_rJja5rjK2rvQicnX2q3u63wF60wA582L4fO_Rhh37syIeFPT8YQh960AYc1YBDr274bnRUDLzl7Ot6tvpmz0N4Xrqv4_TbTEV4YbnHwbZOcC37ytTZoqtj4FzmJU6ZIGrTK8ccK2SZ-8xxykou80GGq2Koa6nKiF_kO4s40rAvrHr42JiwsO01JXK-vWH8zu9b8xur7o_suUFmIXTqe6p9m-qWmrhJxxVROPb8mZ4ugClwc_JIk18jcWhvrH_98xKZj5Q9EurDTIFqhkSDcTA6coqoe3TvC68wrl6xXxth0DZC2PNHCHu1EWDrCGFNFv3aCFHnfwAAAP__&). Plotter provided by dishka.
- discord.py as discord client
