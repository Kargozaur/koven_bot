import inspect
from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any

from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession


def inject_session[**P, R](
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:

    @wraps(func)
    async def wrapper(
        self: object, ctx: commands.Context, *args: P.args, **kwargs: P.kwargs
    ) -> R:
        bot = getattr(self, "bot", None)
        if not bot or not hasattr(bot, "container"):
            raise AttributeError(
                f"{self.__class__.__name__} must have a 'bot' attribute"
            )
        try:
            async with bot.container() as request_container:
                session = await request_container.get(AsyncSession)
                return await func(self, ctx, *args, session=session, **kwargs)
        except Exception as exc:
            print(f"decorator error: {exc}")
            import traceback

            traceback.print_exc()
            raise exc

    sig = inspect.signature(func)
    new_params = [p for p in sig.parameters.values() if p.name != "session"]
    wrapper.__signature__ = sig.replace(parameters=new_params)  # type: ignore
    return wrapper
