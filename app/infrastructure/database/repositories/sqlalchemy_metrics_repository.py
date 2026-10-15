from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.metrics_repository import MetricsRepository
from app.infrastructure.database.models.event import EventModel
from app.infrastructure.database.models.ticket import TicketModel


class SqlAlchemyMetricsRepository(MetricsRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tickets_count(self) -> int:
        query = select(func.count()).select_from(TicketModel)
        return await self.session.scalar(query) or 0

    async def get_cancelled_tickets_count(self) -> int:
        query = (
            select(func.count())
            .select_from(TicketModel)
            .where(TicketModel.status == 'cancelled')
        )
        return await self.session.scalar(query) or 0

    async def get_events_count(self) -> int:
        query = select(func.count()).select_from(EventModel)
        return await self.session.scalar(query) or 0