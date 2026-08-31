from uuid import UUID
from unittest.mock import AsyncMock

import pytest

from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.use_cases.create_ticket import CreateTicketUseCase


@pytest.mark.asyncio
async def test_create_ticket_returns_ticket_id_and_registers_ticket(
    provider,
    ticket_registry,
):
    ticket_id = UUID("1fed0122-b675-42e2-8ae7-49bfb53e8d7f")

    provider.register_ticket = AsyncMock(return_value=ticket_id)

    data = RegisterTicketDTO(
        event_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
        first_name="Ivan",
        last_name="Ivanov",
        seat="A15",
        email="ivan@example.com",
    )

    use_case = CreateTicketUseCase(
        provider=provider,
        ticket_registry=ticket_registry,
    )

    result = await use_case.execute(data)

    assert result == ticket_id

    provider.register_ticket.assert_awaited_once_with(data)

    ticket_registry.add.assert_called_once_with(
        ticket_id=ticket_id,
        event_id=data.event_id,
    )