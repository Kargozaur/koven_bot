import inspect
from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any, Union, get_args, get_origin

from discord.ext import commands
from discord.ext.commands import Context
from dishka import Scope


def inject[**P, R](
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """
    A decorator that injects a dependency from the bot's container
    into the decorated function.

    The dependency is injected into the decorated function as a keyword argument.
    The keyword argument name is inferred from the type hint of the corresponding
    parameter in the decorated function.

    If the parameter is not annotated with a type, or if the type is `None`,
    the parameter is not injected.

    If the parameter is annotated with a `Union`, the first non-`None` type in the union
     is used as the type to inject.

    If the parameter is already present in the decorated function's arguments,
    the value from the arguments is used instead of the injected value.

    If the injection fails
    (for example, if the type cannot be resolved from the container),
    an exception is raised.

    :param P: The parameters of the decorated function.
    :param R: The return type of the decorated function.
    :return: A coroutine that returns the result of the decorated function
    with the injected dependency.
    """

    @wraps(func)
    async def wrapper(
        self: object, ctx: commands.Context, *args: P.args, **kwargs: P.kwargs
    ) -> R:
        bot = getattr(self, "bot", None)
        if not bot or not hasattr(bot, "container"):
            raise AttributeError()
        container = bot.container

        print(f"DEBUG: Entering inject for {wrapper.__name__}")

        async with container(
            scope=Scope.REQUEST, context={Context: ctx}
        ) as request_container:
            sig = inspect.signature(func)
            bound = sig.bind_partial(self, ctx, *args, **kwargs)

            for name, param in sig.parameters.items():
                if name in ("self", "ctx"):
                    continue

                annotation = param.annotation
                if annotation is inspect.Parameter.empty:
                    continue

                origin = get_origin(annotation)
                if origin is Union:
                    args_ = get_args(annotation)
                    annotation = next(
                        (a for a in args_ if a is not type(None)),
                        annotation,
                    )

                if name in bound.arguments and bound.arguments[name] is not None:
                    continue

                try:
                    dependency = await request_container.get(annotation)
                    bound.arguments[name] = dependency
                    print(f"DEBUG: Injected {name}")
                except Exception as e:
                    print(f"[DECORATOR] {name} injection failed: {e}")

            return await func(*bound.args, **bound.kwargs)

    return wrapper
