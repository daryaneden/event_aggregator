from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.entities.event import Event
from app.domain.entities.sync_state import SyncState


class EventRepository(ABC):

    @abstractmethod
    async def save(self, event: Event) -> None:
        pass
