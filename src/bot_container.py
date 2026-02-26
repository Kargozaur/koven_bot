import pathlib

import discord
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

    async def on_message(self, message: discord.Message) -> None:
        print(f"DEBUG: Processing message: '{message.content}'")
        if message.author.bot:
            return

        # Пытаемся понять, считает ли discord.py это командой
        ctx = await self.get_context(message)
        if ctx.valid:
            print(f"DEBUG: Command '{ctx.command}' found, invoking...")
        else:
            print("DEBUG: No valid command found for this message.")
        await self.process_commands(message)

    async def close(self) -> None:
        await super().close()
        if self.container:
            await self.container.close()
