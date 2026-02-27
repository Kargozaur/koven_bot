from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from httpx import AsyncClient, Timeout


class HttpxProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_async_client(self) -> AsyncIterable[AsyncClient]:
        async with AsyncClient(
            timeout=Timeout(10), headers={"Accept": "application/json"}
        ) as client:
            yield client
