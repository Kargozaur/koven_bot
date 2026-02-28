from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.unit_of_work.unit_of_work import UnitOfWork


class UOWProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> UnitOfWork:
        print("injecting uow")
        uow = UnitOfWork(session)
        print("injected uow")
        return uow
