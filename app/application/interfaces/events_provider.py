from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.application.dtos.events_page import EventsPage


class EventsProvider(ABC):

    @abstractmethod
    async def get_events_page(self, 
                              changed_at: datetime, 
                              url: str | None = None) -> EventsPage:
        pass

    @abstractmethod
    async def get_available_seats(self,
        event_id: UUID) -> list[str] | None: pass

    @abstractmethod
    async def register_ticket(self) -> UUID:
        pass

    @abstractmethod
    async def cancel_ticket(self, ticket_id: UUID) -> bool:
        pass