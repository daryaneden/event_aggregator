from app.application.interfaces.uow import UnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: AsyncSession):
        self.session = session

        self.event_repository = SqlAlchemyEventRepository(
            session
        )

        self.sync_state_repository = SqlAlchemySyncStateRepository(
            session
        )

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()