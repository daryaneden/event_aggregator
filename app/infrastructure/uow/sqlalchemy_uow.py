from app.infrastructure.database.database import AsyncSessionFactory
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.event_repository import EventRepository
from app.application.interfaces.sync_state_repository import SyncStateRepository
from app.application.interfaces.uow import UnitOfWork
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: AsyncSession, 
                 event_repository: EventRepository, 
                 sync_state_repository: SyncStateRepository):
        self.session = session

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

#     def __init__(self):
#         self.session = AsyncSessionFactory()

#         self.event_repository = SqlAlchemyEventRepository(
#             self.session
#         )

#         self.sync_state_repository = (
#             SqlAlchemySyncStateRepository(
#                 self.session
#             )
#         )

#     async def __aenter__(self):
#         await self.session.begin()
#         return self

#     async def __aexit__(
#         self,
#         exc_type,
#         exc_value,
#         traceback,
#     ):
#         try:
#             if exc_type is not None:
#                 await self.session.rollback()
#             else:
#                 await self.session.commit()
#         finally:
#             await self.session.close()