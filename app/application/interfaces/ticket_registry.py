from abc import ABC, abstractmethod
from uuid import UUID


class TicketRegistry(ABC):

    @abstractmethod
    def add(self, ticket_id: UUID, event_id: UUID) -> None:
        pass

    @abstractmethod
    def get_event_id(self, ticket_id: UUID) -> UUID | None:
        pass

    @abstractmethod
    def remove(self, ticket_id: UUID) -> None:
        pass