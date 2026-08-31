from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from app.application.dtos.events_page import EventsPage
from app.application.dtos.register_ticket import RegisterTicketDTO


class EventsProvider(ABC):

    @abstractmethod
    async def get_events_page(self, changed_at: datetime, url: str | None = None) -> EventsPage:
        pass

    @abstractmethod
    async def get_available_seats(
        self,
        event_id: UUID,
    ) -> list[str] | None:
        pass

    async def register_ticket(
    self,
    data: RegisterTicketDTO) -> UUID:
        pass