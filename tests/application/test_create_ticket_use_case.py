from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from app.application.dtos.register_ticket import RegisterTicketDTO
from app.application.use_cases.create_ticket import CreateTicketUseCase
from app.domain.entities.ticket import Ticket

@pytest.mark.asyncio
async def test_create_ticket_returns_ticket_id_and_saves_ticket_and_outbox_message(
    provider,
    uow_factory,
    unit_of_work
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
    unit_of_work.outbox_repository.save.assert_awaited_once()

    saved_ticket = unit_of_work.ticket_repository.save.await_args.args[0]
    saved_message = (unit_of_work.outbox_repository.save.await_args.args[0])
    

    assert saved_ticket.id == ticket_id
    assert saved_ticket.event_id == data.event_id
    assert saved_ticket.first_name == data.first_name
    assert saved_ticket.last_name == data.last_name
    assert saved_ticket.seat == data.seat
    assert saved_ticket.email == data.email

    assert saved_message.event_type == "ticket_registered"
    assert saved_message.payload["ticket_id"] == str(ticket_id)
    assert saved_message.payload["event_id"] == str(data.event_id)
    assert saved_message.payload["first_name"] == data.first_name
    assert saved_message.payload["last_name"] == data.last_name
    assert saved_message.payload["email"] == data.email
    assert saved_message.payload["seat"] == data.seat

@pytest.mark.asyncio
async def test_create_ticket_does_not_save_ticket_or_outbox_when_provider_fails(
    provider,
    uow_factory,
    unit_of_work,
):
    provider.register_ticket = AsyncMock(
        side_effect=RuntimeError("provider failed"),
    )

    data = RegisterTicketDTO(
        event_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
        first_name="Ivan",
        last_name="Ivanov",
        seat="A15",
        email="ivan@example.com",
    )

    use_case = CreateTicketUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    with pytest.raises(RuntimeError, match="provider failed"):
        await use_case.execute(data)

    provider.register_ticket.assert_awaited_once_with(data)

    unit_of_work.ticket_repository.save.assert_not_awaited()
    unit_of_work.outbox_repository.save.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_ticket_returns_existing_ticket_for_same_idempotency_key(
    provider,
    uow_factory,
    unit_of_work,
):
    existing_ticket = Ticket(
        id=uuid4(),
        event_id=uuid4(),
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        seat="A1",
    )

    data = RegisterTicketDTO(
        event_id=existing_ticket.event_id,
        first_name=existing_ticket.first_name,
        last_name=existing_ticket.last_name,
        email=existing_ticket.email,
        seat=existing_ticket.seat,
        idempotency_key="test-key",
    )

    unit_of_work.ticket_repository.get_by_idempotency_key = AsyncMock(
        return_value=existing_ticket,
    )

    use_case = CreateTicketUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    result = await use_case.execute(data)

    assert result == existing_ticket.id

    provider.register_ticket.assert_not_awaited()
    unit_of_work.ticket_repository.save.assert_not_awaited()
    unit_of_work.outbox_repository.save.assert_not_awaited()

    unit_of_work.ticket_repository.get_by_idempotency_key.assert_awaited_once_with("test-key")
