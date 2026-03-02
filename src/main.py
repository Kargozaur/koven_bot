import asyncio

from dishka import make_async_container  # , plotter
from dishka.async_container import AsyncContainer

from src.bot_container import BotContainer
from src.core.settings.settings import Settings
from src.di_providers.database_provider import DBProvider
from src.di_providers.httpx_provider import HttpxProvider
from src.di_providers.repo_provider import RepositoryProvider
from src.di_providers.service_provider import ServiceProvider
from src.di_providers.settings_provider import SettingsProvider
from src.di_providers.uow_provider import UOWProvider
from src.di_providers.update_provider import UpdateProvider


async def main() -> None:
    container: AsyncContainer = make_async_container(
        SettingsProvider(),
        DBProvider(),
        HttpxProvider(),
        RepositoryProvider(),
        UOWProvider(),
        ServiceProvider(),
        UpdateProvider(),
    )
    settings: Settings = await container.get(Settings)

    intents = __import__("discord").Intents.default()
    intents.message_content = True

    bot = BotContainer(command_prefix="!", intents=intents)
    bot.container: AsyncContainer = container
    # print(plotter.render_d2(container))  # build a dependency graph
    try:
        await bot.start(settings.discord.token.get_secret_value())
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
