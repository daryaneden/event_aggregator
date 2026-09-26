from uuid import uuid4, UUID

import pytest

from app.domain.entities.ticket import Ticket

@pytest.mark.asyncio
async def test_get_ticket_by_idempotency_key(
    test_session,
    provider_event,
    ticket_repository,
    create_event,
):
    await create_event(test_session, provider_event)

    ticket = Ticket(
        id=uuid4(),
        event_id=UUID(provider_event["id"]),
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        seat="A1",
    )

    await ticket_repository.save(
        ticket,
        idempotency_key="test-key",
    )
    await test_session.commit()

    result = await ticket_repository.get_by_idempotency_key(
        "test-key",
    )

    assert result is not None
    assert result.id == ticket.id
    assert result.event_id == ticket.event_id
    assert result.first_name == ticket.first_name
    assert result.last_name == ticket.last_name
    assert result.email == ticket.email
    assert result.seat == ticket.seat