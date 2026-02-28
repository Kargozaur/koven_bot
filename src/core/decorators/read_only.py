from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any

from src.unit_of_work.unit_of_work import UnitOfWork


def read_only[**P, R](
    func: Callable[..., Coroutine[Any, Any, R]] | Callable[..., Awaitable[R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """
    A decorator that marks a function as read-only.

    A read-only function is a function that reads data from the database
    but does not modify it. It is useful for functions that need to
    query the database but do not need to modify its data.

    The decorator will automatically commit the transaction if the function
    completes successfully, or rollback if an exception is raised.

    The function should take a session as a keyword argument, and the decorator
    will use this session to create a UnitOfWork. If no session is
    provided, an AttributeError will be raised.

    :param P: The parameters of the decorated function.
    :param R: The return type of the decorated function.
    :return: A coroutine that returns the result of the decorated function
    with the injected dependency.
    """

    @wraps(func)
    async def wrapper(self: object, *args: P.args, **kwargs: P.kwargs) -> R:
        if not hasattr(self, "UoW"):
            raise AttributeError("Unit of work must be provided")
        uow: UnitOfWork = self.UoW  # ty:ignore[invalid-assignment]
        async with uow:
            try:
                return await func(self, *args, **kwargs)
            except Exception as exc:
                raise exc

    return wrapper
