from app.application.dtos.business_metrics import BusinessMetricsDto
from app.application.interfaces.metrics_repository import MetricsRepository


class GetBusinessMetricsUseCase:
    def __init__(self, repository: MetricsRepository):
        self.repository = repository

    async def execute(self) -> BusinessMetricsDto:
        tickets_count = await self.repository.get_tickets_count()
        cancelled_tickets_count = await self.repository.get_cancelled_tickets_count()
        events_count = await self.repository.get_events_count()

        return BusinessMetricsDto(tickets_count=tickets_count,
                               cancelled_tickets_count=cancelled_tickets_count,
                               events_count=events_count)