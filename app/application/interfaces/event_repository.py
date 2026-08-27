from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from app.domain.entities.event import Event

class EventRepository(ABC):

    @abstractmethod
    async def save(self, event: Event) -> None:
        pass

    @abstractmethod
    async def get_events(
        self,
        date_from: date | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Event], int]:
        pass

    @abstractmethod
    async def get_by_id(self, event_id: UUID) -> Event | None:
        pass
