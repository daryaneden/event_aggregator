from uuid import UUID

from app.application.exceptions import TicketNotFoundException
from app.application.interfaces.events_provider import EventsProvider
from app.application.interfaces.ticket_repository import TicketRepository


class CancelTicketUseCase:

    def __init__(self,
        provider: EventsProvider,
        ticket_repository: TicketRepository):

        self.provider = provider
        self.ticket_registry = ticket_repository

    async def execute(self, ticket_id: UUID) -> None:

        async with self.uow_factory() as uow:
            ticket = await uow.ticket_repository.get_by_id(ticket_id)

            if ticket is None:
                raise TicketNotFoundException(ticket_id)

            await self.provider.cancel_ticket(event_id=ticket.event_id,
                                              ticket_id=ticket_id)