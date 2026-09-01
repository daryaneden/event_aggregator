from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.event_repository import EventRepository
from app.application.interfaces.sync_state_repository import SyncStateRepository
from app.application.interfaces.uow import UnitOfWork

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

    async def __aexit__(self, exc_type, exc_value, traceback):
        
        try:
            if exc_type is not None:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()

