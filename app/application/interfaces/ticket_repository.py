from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.ticket import Ticket


class TicketRepository(ABC):

    @abstractmethod
    async def save(self, ticket: Ticket, idempotency_key: str | None = None) -> None:
        pass

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key: str) -> Ticket | None:
        pass

    @abstractmethod
    async def get_by_id(self, ticket_id: UUID) -> Ticket | None:
        pass