from uuid import UUID

from app.application.interfaces.ticket_registry import TicketRegistry


class InMemoryTicketRegistry(TicketRegistry):

    def __init__(self):
        self._tickets: dict[UUID, UUID] = {}

    def add(self, ticket_id: UUID, event_id: UUID) -> None:
        self._tickets[ticket_id] = event_id

    def get_event_id(self, ticket_id: UUID) -> UUID | None:
        return self._tickets.get(ticket_id)

    def remove(self, ticket_id: UUID) -> None:
        self._tickets.pop(ticket_id, None)