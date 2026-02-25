from discord.ext import commands

from src.bot_container import BotContainer
from src.core.settings.db_settings import AbstractDBConfig


class DBCog(commands.Cog):
    def __init__(self, bot: BotContainer) -> None:
        self.bot = bot

    @commands.command()
    async def check_db(self, ctx: commands.Context) -> None:
        config = await self.bot.container.get(AbstractDBConfig)
        await ctx.send(f"DB ready {config.dsn}")
