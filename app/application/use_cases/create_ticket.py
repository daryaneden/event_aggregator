from uuid import UUID

from app.application.dtos.outbox_message import OutboxMessageDto
from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.exceptions import TicketIdempotencyConflict
from app.application.interfaces.events_provider import EventsProvider
from app.application.interfaces.uow_factory import UnitOfWorkFactory
from app.domain.entities.ticket import Ticket


class CreateTicketUseCase:

    def __init__(self, provider: EventsProvider, 
                 uow_factory: UnitOfWorkFactory):
        
        self.provider = provider
        self.uow_factory = uow_factory

    async def execute(self, data: RegisterTicketDTO) -> UUID:

        async with self.uow_factory() as uow:

            if data.idempotency_key:
                existing_ticket = (
                    await uow.ticket_repository.get_by_idempotency_key(
                        data.idempotency_key,
                    )
                )

                if existing_ticket:
                    if not self._is_same_request(data, existing_ticket):
                        raise TicketIdempotencyConflict()

                    return existing_ticket.id

            ticket_id = await self.provider.register_ticket(data)

            ticket = Ticket(
                id=ticket_id,
                event_id=data.event_id,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                seat=data.seat,
            )

            await uow.ticket_repository.save(
                ticket,
                idempotency_key=data.idempotency_key,
            )

            await uow.outbox_repository.save(
                OutboxMessageDto(
                    event_type="ticket_registered",
                    payload={
                        "ticket_id": str(ticket_id),
                        "event_id": str(data.event_id),
                        "first_name": data.first_name,
                        "last_name": data.last_name,
                        "email": data.email,
                        "seat": data.seat}))

            return ticket_id

    def _is_same_request(self, data: RegisterTicketDTO, ticket: Ticket) -> bool:
        return (ticket.event_id == data.event_id
            and ticket.first_name == data.first_name
            and ticket.last_name == data.last_name
            and ticket.email == data.email
            and ticket.seat == data.seat)