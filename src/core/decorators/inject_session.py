from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any, Protocol, cast

from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession


class BotProto(Protocol):
    bot: Any


def inject_session[**P, R](
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:

    @wraps(func)
    async def wrapper(ctx: commands.Context, *args: P.args, **kwargs: P.kwargs) -> R:
        if not args:
            raise IndexError("Decorator used on a function without the arguments")
        self = cast(BotProto, args[0])
        if not hasattr(self, "bot"):
            raise IndexError(f"{self.__class__.__name__} must have a 'bot' attribute")
        async with self.bot.container.request() as request_container:
            session = await request_container.get(AsyncSession)
        return await func(ctx, *args, session=session, **kwargs)

    return wrapper
