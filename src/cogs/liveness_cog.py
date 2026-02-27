import time

from discord.ext import commands
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.decorators.inject_session import inject


class LivenessCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        import traceback

        print(f"Error: {self.qualified_name}:")
        traceback.print_exc()
        await ctx.send(f"Error: {error}")

    @commands.command(name="ping")
    @inject
    async def ping(
        self,
        ctx: commands.Context,
        session: AsyncSession | None = None,
    ) -> None:
        if session is None:
            return
        db_start = time.perf_counter()
        await session.execute(text("SELECT 1"))
        db_end = time.perf_counter()
        db_ms = round((db_end - db_start) * 1000)

        latency = round(self.bot.latency * 1000)
        await ctx.send(
            f"Pong. Discord latency: {latency} ms. \nDatabase ready. \n"
            f"DB delay: {db_ms} ms"
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LivenessCog(bot))
