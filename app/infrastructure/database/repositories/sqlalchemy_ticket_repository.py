from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.ticket_repository import TicketRepository
from app.domain.entities.ticket import Ticket
from app.infrastructure.database.models.ticket import TicketModel


class SqlAlchemyTicketRepository(TicketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, ticket: Ticket, idempotency_key: str | None = None) -> None:
        model = TicketModel(id=ticket.id,
            event_id=ticket.event_id,
            first_name=ticket.first_name,
            last_name=ticket.last_name,
            email=ticket.email,
            seat=ticket.seat,
            idempotency_key=idempotency_key)

        self.session.add(model)

    async def get_by_idempotency_key(self, idempotency_key: str) -> Ticket | None:
        result = await self._session.execute(select(TicketModel).where(TicketModel.idempotency_key == idempotency_key))

        ticket_model = result.scalar_one_or_none()

        if ticket_model is None:
            return None

        return Ticket(id=ticket_model.id,
            event_id=ticket_model.event_id,
            first_name=ticket_model.first_name,
            last_name=ticket_model.last_name,
            email=ticket_model.email,
            seat=ticket_model.seat)