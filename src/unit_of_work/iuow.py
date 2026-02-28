from typing import Protocol, Self


class IUnitOfWork(Protocol):
    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: BaseException,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
