from discord.ext import commands

from src.bot_container import BotContainer
from src.core.decorators.inject_session import inject
from src.entities.schemas.character import CharacterDTO
from src.repositories.character_repo import CharacterRepository
from src.services.rio_service import RaiderIOService


class RioCog(commands.Cog):
    def __init__(self, bot: BotContainer) -> None:
        self.bot = bot

    @commands.command(name="add")
    @inject
    async def link(
        self,
        ctx: commands.Context,
        url: str,
        rio: RaiderIOService = commands.parameter(default=None),
        repo: CharacterRepository = commands.parameter(default=None),
    ) -> None:
        params = rio._extract_params_from_url(url)
        if not params:
            await ctx.send("Bad url")
            return

        data = await rio.fetch_character(params)

        if not data:
            await ctx.send("Character not found")
            return

        try:
            dto = CharacterDTO(
                name=data["name"],
                region=data["region"],
                realm=data["realm"],
            )

            await repo.save_character(ctx.author.id, dto)

            await ctx.send(
                f":white_check_mark: Added character: {data['name']}.\n"
                f"Owner: {ctx.author.mention}"
            )

        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()


async def setup(bot: BotContainer) -> None:
    await bot.add_cog(RioCog(bot))
