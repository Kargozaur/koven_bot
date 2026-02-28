import asyncio

import discord
from discord.ext import commands

from src.bot_container import BotContainer
from src.core.decorators.inject import inject
from src.entities.schemas.character import CharacterDTO, CharacterResponse
from src.params.char_params import CharParamns
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
        params: CharParamns | None = await asyncio.to_thread(
            rio._extract_params_from_url, url
        )
        if not params:
            await ctx.send("Bad url")
            return

        data = await rio.fetch_character(params)

        if not data:
            await ctx.send("Character not found")
            return

        try:
            dto = CharacterDTO(
                character_name=data["name"],
                region=data["region"],
                realm=data["realm"],
                url=data["profile_url"],
                achievement_points=data["achievement_points"],
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

    @commands.command(name="get_me")
    @inject
    async def build_info(
        self,
        ctx: commands.Context,
        repo: CharacterRepository = commands.parameter(default=None),
    ) -> None:
        characters: list[CharacterResponse] = await repo.get_characters(ctx.author.id)
        embed = discord.Embed(
            title=f"Characters of {ctx.author.name}", color=discord.Color.blue()
        )
        if not characters:
            embed.description = "You have no characters"
        else:
            for char in characters:
                link: str = (
                    f"[Profile]({char.url}) - {char.realm_name} - "
                    f"({char.region.upper()})"
                    if char.url
                    else f"{char.realm_name} - ({char.region.upper()})"
                )
                embed.add_field(
                    name=char.name,
                    value=link,
                    inline=False,
                )
        await ctx.send(embed=embed)


async def setup(bot: BotContainer) -> None:
    await bot.add_cog(RioCog(bot))
