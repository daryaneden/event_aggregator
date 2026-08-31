from uuid import UUID
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.cancel_ticket import CancelTicketUseCase
from app.application.exceptions import TicketNotFoundException

@pytest.mark.asyncio
async def test_cancel_ticket_cancels_ticket_and_removes_it(
    provider,
    ticket_registry,
):
    ticket_id = UUID("1fed0122-b675-42e2-8ae7-49bfb53e8d7f")
    event_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    ticket_registry.get_event_id.return_value = event_id
    provider.cancel_ticket = AsyncMock()

    use_case = CancelTicketUseCase(
        provider=provider,
        ticket_registry=ticket_registry,
    )

    await use_case.execute(ticket_id)

    ticket_registry.get_event_id.assert_called_once_with(ticket_id)

    provider.cancel_ticket.assert_awaited_once_with(
        event_id=event_id,
        ticket_id=ticket_id,
    )

    ticket_registry.remove.assert_called_once_with(ticket_id)

@pytest.mark.asyncio
async def test_cancel_ticket_raises_exception_when_ticket_not_found(
    provider,
    ticket_registry,
):
    ticket_id = UUID("1fed0122-b675-42e2-8ae7-49bfb53e8d7f")

    ticket_registry.get_event_id.return_value = None

    use_case = CancelTicketUseCase(
        provider=provider,
        ticket_registry=ticket_registry,
    )

    with pytest.raises(TicketNotFoundException):
        await use_case.execute(ticket_id)

    provider.cancel_ticket.assert_not_called()
    ticket_registry.remove.assert_not_called()