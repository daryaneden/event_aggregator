from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.use_cases.create_ticket import CreateTicketUseCase


@pytest.mark.asyncio
async def test_create_ticket_returns_ticket_id_and_saves_ticket(
    provider,
    uow_factory,
    unit_of_work,
):
    ticket_id = UUID('1fed0122-b675-42e2-8ae7-49bfb53e8d7f')

    provider.register_ticket = AsyncMock(return_value=ticket_id)

    data = RegisterTicketDTO(
        event_id=UUID('550e8400-e29b-41d4-a716-446655440000'),
        first_name='Ivan',
        last_name='Ivanov',
        seat='A15',
        email='ivan@example.com',
    )

    use_case = CreateTicketUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    result = await use_case.execute(data)

    assert result == ticket_id

    provider.register_ticket.assert_awaited_once_with(data)
    unit_of_work.ticket_repository.save.assert_awaited_once()

    saved_ticket = unit_of_work.ticket_repository.save.await_args.args[0]

    assert saved_ticket.id == ticket_id
    assert saved_ticket.event_id == data.event_id
    assert saved_ticket.first_name == data.first_name
    assert saved_ticket.last_name == data.last_name
    assert saved_ticket.seat == data.seat
    assert saved_ticket.email == data.email
