import discord
from discord.ext import commands

from src.bot_container import BotContainer
from src.core.decorators.inject import inject
from src.core.settings.db_settings import AbstractDBConfig
from src.entities.schemas.character import CharacterResponse
from src.services.character_service import CharacterService
from src.services.owner_service import OwnerService


class DBCog(commands.Cog):
    def __init__(self, bot: BotContainer) -> None:
        self.bot = bot

    @commands.command(name="which_db")
    async def check_db(self, ctx: commands.Context) -> None:
        config = await self.bot.container.get(AbstractDBConfig)
        await ctx.send(f"DB ready: {config.dsn.split('+')[0]}")

    @commands.command(name="get_me")
    @inject
    async def build_info(
        self,
        ctx: commands.Context,
        svc: CharacterService = commands.parameter(default=None),
    ) -> None:
        characters: list[CharacterResponse] = await svc.get_characters(ctx.author.id)
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

    @commands.command(name="delete")
    @inject
    async def delete_character(
        self,
        ctx: commands.Context,
        *,
        character_name: str,
        svc: CharacterService = commands.parameter(default=None),
    ) -> None:
        name: str = character_name.strip().capitalize()
        result: bool | None | str = await svc.delete_character(ctx.author.id, name)
        if result is True:
            await ctx.send("Character deleted")
        else:
            await ctx.send(f"Character not found: {result}")

    @commands.command(name="delete_owner")
    @inject
    async def delete_owner(
        self,
        ctx: commands.Context,
        *,
        owner_id: int,
        svc: OwnerService = commands.parameter(default=None),
    ) -> None:
        result: bool | None = await svc.deactivate_owner(owner_id)
        if result is True:
            await ctx.send("Owner deleted")
        else:
            await ctx.send("Owner not found")


async def setup(bot: BotContainer) -> None:
    await bot.add_cog(DBCog(bot))
