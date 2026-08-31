from uuid import UUID

from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.interfaces.event_provider import EventsProvider
from app.application.interfaces.ticket_registry import TicketRegistry


class CreateTicketUseCase:

    def __init__(self, provider: EventsProvider, ticket_registry: TicketRegistry):
        self.provider = provider
        self.ticket_registry = ticket_registry

    async def execute(self, data: RegisterTicketDTO) -> UUID:
        ticket_id = await self.provider.register_ticket(data)

        self.ticket_registry.add(
            ticket_id=ticket_id,
            event_id=data.event_id,
        )

        return ticket_id