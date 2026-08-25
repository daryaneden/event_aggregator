from app.application.interfaces.event_repository import EventRepository
from app.domain.entities.event import Event
from app.domain.entities.sync_state import SyncState
from datetime import datetime
from app.infrastructure.database.models.sync_state import SyncStateModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class SqlAlchemyEventRepository(EventRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, event: Event) -> None:
        pass
