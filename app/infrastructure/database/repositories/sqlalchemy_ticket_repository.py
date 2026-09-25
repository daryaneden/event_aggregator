from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.ticket import Ticket
from app.application.interfaces.ticket_repository import TicketRepository
from app.infrastructure.database.models.ticket import TicketModel


class SqlAlchemyTicketRepository(TicketRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, ticket: Ticket) -> None:
        model = TicketModel(id=ticket.id,
            event_id=ticket.event_id,
            first_name=ticket.first_name,
            last_name=ticket.last_name,
            email=ticket.email,
            seat=ticket.seat)

        self.session.add(model)