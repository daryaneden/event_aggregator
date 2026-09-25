from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket


class TicketRepository(ABC):

    @abstractmethod
    async def save(self, ticket: Ticket) -> None:
        pass