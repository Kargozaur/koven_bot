import asyncio

from discord.ext import commands, tasks

from src.bot_container import BotContainer
from src.core.decorators.inject import inject
from src.entities.schemas.character import CharacterDTO
from src.params.char_params import CharParamns
from src.polling.character_updater import CharacterUpdater
from src.services.character_service import CharacterService
from src.services.rio_service import RaiderIOService


class RioCog(commands.Cog):
    def __init__(self, bot: BotContainer) -> None:
        self.bot = bot
        self.polling_task.start()

    def cog_unload(self):  # noqa: ANN201
        self.polling_task.cancel()

    @tasks.loop(minutes=30)
    async def polling_task(self) -> None:
        print("updating db")
        container = self.bot.container
        async with container() as request_container:
            updater: CharacterUpdater = await request_container.get(CharacterUpdater)
            await updater.update_characters()
        print("updated db")

    @polling_task.before_loop
    async def before_polling(self) -> None:
        await self.bot.wait_until_ready()

    @commands.command(name="add")
    @inject
    async def link(
        self,
        ctx: commands.Context,
        url: str,
        rio: RaiderIOService = commands.parameter(default=None),
        svc: CharacterService = commands.parameter(default=None),
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

            result = await svc.create_character(ctx.author.id, dto)
            if result is not None:
                await ctx.send(f"You can't add characters: {result}")
            else:
                await ctx.send(
                    f":white_check_mark: Added character: {data['name']}.\n"
                    f"Owner: {ctx.author.mention}"
                )

        except Exception as e:
            print(f"Error: {e}")
            import traceback

            traceback.print_exc()

    @commands.command(name="force_update")
    @inject
    async def force_update(
        self,
        ctx: commands.Context,
        updater: CharacterUpdater = commands.parameter(default=None),
    ) -> None:
        print("Updating db")
        await updater.update_characters()
        print("updated db")
        await ctx.send(":white_check_mark: updated db")


async def setup(bot: BotContainer) -> None:
    await bot.add_cog(RioCog(bot))
