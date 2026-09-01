from datetime import date

from app.application.interfaces.event_repository import EventRepository
from app.domain.entities.event import Event


class GetEventsUseCase:

    def __init__(self, event_repository: EventRepository):

        self.event_repository = event_repository

    async def execute(self, date_from: date | None,
                      page: int,
                      page_size: int) -> tuple[list[Event], int]:

        return await self.event_repository.get_events(
            date_from=date_from,
            page=page,
            page_size=page_size,
        )