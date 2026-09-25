from abc import ABC, abstractmethod

from app.application.interfaces.event_repository import EventRepository
from app.application.interfaces.sync_state_repository import SyncStateRepository
from app.application.interfaces.ticket_repository import TicketRepository
from app.application.interfaces.outbox_repository import OutboxRepository

class UnitOfWork(ABC):

    event_repository: EventRepository
    sync_state_repository: SyncStateRepository
    ticket_repository: TicketRepository
    outbox_repository: OutboxRepository

    async def __aenter__(self):
        return self

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass
