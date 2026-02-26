import asyncio

from dishka import make_async_container
from dishka.async_container import AsyncContainer

from src.bot_container import BotContainer
from src.core.settings.settings import Settings
from src.di_containers.database_container import DBProvider
from src.di_containers.httpx_container import AsyncClientProvider
from src.di_containers.repo_containers import RepositoryProvider
from src.di_containers.rio_container import RioContainer
from src.di_containers.settings_container import SettingsProvider


async def main() -> None:
    container: AsyncContainer = make_async_container(
        SettingsProvider(),
        DBProvider(),
        AsyncClientProvider(),
        RepositoryProvider(),
        RioContainer(),
    )
    settings: Settings = await container.get(Settings)

    intents = __import__("discord").Intents.default()
    intents.message_content = True

    bot = BotContainer(command_prefix="!", intents=intents)
    bot.container: AsyncContainer = container

    try:
        await bot.start(settings.discord.token.get_secret_value())
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
