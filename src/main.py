import asyncio

from dishka import make_async_container
from dishka.async_container import AsyncContainer

from src.bot_container import BotContainer
from src.core.settings.settings import Settings
from src.di_containers.database_container import DBContainer
from src.di_containers.httpx_container import AsyncClientContainer
from src.di_containers.repo_containers import RepositoryContainer
from src.di_containers.rio_container import RioContainer
from src.di_containers.settings_container import SettingsContainer


async def main() -> None:
    container: AsyncContainer = make_async_container(
        SettingsContainer(),
        DBContainer(),
        AsyncClientContainer(),
        RepositoryContainer(),
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
