import pathlib

from discord.ext import commands
from dishka.async_container import AsyncContainer


class BotContainer(commands.Bot):
    container: AsyncContainer

    async def setup_hook(self) -> None:
        cogs_path = pathlib.Path(__file__).parent / "cogs"

        for file in cogs_path.glob("*.py"):
            if file.name == "__init__.py":
                continue

            extension = f"src.cogs.{file.stem}"
            try:
                await self.load_extension(extension)
                print(f"loaded: {extension}")
            except Exception as exc:
                print(f"Failed to load extension: {exc}")
