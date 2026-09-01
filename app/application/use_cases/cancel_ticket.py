from uuid import UUID

from app.application.exceptions import TicketNotFoundException
from app.application.interfaces.events_provider import EventsProvider
from app.application.interfaces.ticket_registry import TicketRegistry


class CancelTicketUseCase:

    def __init__(self,
        provider: EventsProvider,
        ticket_registry: TicketRegistry):

        self.provider = provider
        self.ticket_registry = ticket_registry

    async def execute(self, ticket_id: UUID) -> None:

        event_id = self.ticket_registry.get_event_id(ticket_id)

        if event_id is None:
            raise TicketNotFoundException(ticket_id)

        await self.provider.cancel_ticket(
            event_id=event_id,
            ticket_id=ticket_id,
        )

        self.ticket_registry.remove(ticket_id)