from discord.ext import commands
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.decorators.inject_session import inject_session


class LivenessCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping")
    @inject_session
    async def ping(self, ctx: commands.Context, *, session: AsyncSession) -> None:
        try:
            await session.execute(text("SELECT 1"))
            db_status = "DB ready"
        except Exception as exc:
            db_status = f"DB is not ready: {exc}"

        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong. Latency: {latency}. Database: {db_status}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LivenessCog(bot))
