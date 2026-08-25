from abc import ABC, abstractmethod
from datetime import datetime
from app.application.models.events_page import EventsPage


class EventsProvider(ABC):

    @abstractmethod
    async def get_events_page(self, changed_at: datetime, url: str | None = None) -> EventsPage:
        pass
    