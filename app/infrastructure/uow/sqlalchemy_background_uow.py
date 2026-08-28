from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.uow import UnitOfWork
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository

class SqlAlchemyBackgroundUnitOfWork(UnitOfWork):

    def __init__(self, factory: AsyncSession, event_repository, sync_state_repository):

        self.session = factory
        self.event_repository = event_repository
        self.sync_state_repository = sync_state_repository

    async def __aenter__(self):
        await self.session.begin()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()