from uuid import UUID

from app.application.dtos.outbox_message import OutboxMessageDto
from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.interfaces.events_provider import EventsProvider
from app.application.interfaces.uow_factory import UnitOfWorkFactory
from app.domain.entities.ticket import Ticket


class CreateTicketUseCase:

    def __init__(self, provider: EventsProvider, 
                 uow_factory: UnitOfWorkFactory):
        
        self.provider = provider
        self.uow_factory = uow_factory

    async def execute(self, data: RegisterTicketDTO) -> UUID:

        ticket_id = await self.provider.register_ticket(data)

        ticket = Ticket(id=ticket_id,
            event_id=data.event_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            seat=data.seat)

        async with self.uow_factory() as uow:
            await uow.ticket_repository.save(ticket)

            await uow.outbox_repository.save(OutboxMessageDto(event_type="ticket_registered",
                                                               payload={"ticket_id": str(ticket.id),
                                                                        "event_id": str(ticket.event_id),
                                                                        "first_name": ticket.first_name,
                                                                        "last_name": ticket.last_name,
                                                                        "email": ticket.email,
                                                                        "seat": ticket.seat}))

        return ticket_id