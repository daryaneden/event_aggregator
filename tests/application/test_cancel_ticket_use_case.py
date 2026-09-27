from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from app.application.exceptions import TicketNotFoundException
from app.application.use_cases.cancel_ticket import CancelTicketUseCase
from app.domain.entities.ticket import Ticket

@pytest.mark.asyncio
async def test_cancel_ticket_cancels_ticket(provider,
                                            uow_factory,
                                            unit_of_work):
    
    ticket_id = UUID("1fed0122-b675-42e2-8ae7-49bfb53e8d7f")
    event_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    ticket = Ticket(id=ticket_id,
                    event_id=event_id,
                    first_name="John",
                    last_name="Doe",
                    email="john@example.com",
                    seat="A1")

    unit_of_work.ticket_repository.get_by_id = AsyncMock(return_value=ticket)

    provider.cancel_ticket = AsyncMock()

    use_case = CancelTicketUseCase(provider=provider,
                                   uow_factory=uow_factory)

    await use_case.execute(ticket_id)

    unit_of_work.ticket_repository.get_by_id.assert_awaited_once_with(ticket_id)

    provider.cancel_ticket.assert_awaited_once_with(event_id=event_id,
                                                    ticket_id=ticket_id)

@pytest.mark.asyncio
async def test_cancel_ticket_raises_exception_when_ticket_not_found(provider,
                                                                    ticket_repository):
    ticket_id = UUID('1fed0122-b675-42e2-8ae7-49bfb53e8d7f')

    ticket_repository.get_event_id.return_value = None

    use_case = CancelTicketUseCase(provider=provider,
                                   ticket_repository=ticket_repository)

    with pytest.raises(TicketNotFoundException):
        await use_case.execute(ticket_id)

    provider.cancel_ticket.assert_not_called()
    ticket_repository.remove.assert_not_called()