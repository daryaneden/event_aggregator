from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork


class SqlAlchemyUnitOfWorkFactory:

    def __init__(self, session_factory: async_sessionmaker[AsyncSession],
                 uow_builder: Callable[[AsyncSession], SqlAlchemyUnitOfWork]):
        
        self._session_factory = session_factory
        self._uow_builder = uow_builder

    def __call__(self) -> SqlAlchemyUnitOfWork:
        
        session = self._session_factory()
        return self._uow_builder(session)