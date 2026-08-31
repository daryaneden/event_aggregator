from uuid import UUID

from app.application.exceptions import EventNotFoundException
from app.application.interfaces.event_repository import EventRepository
from app.domain.entities.event import Event


class GetEventUseCase:

    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def execute(self, event_id: UUID) -> Event:
        event = await self.event_repository.get_by_id(event_id)

        if event is None:
            raise EventNotFoundException(event_id)

        return event