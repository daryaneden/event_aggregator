from uuid import uuid4

import pytest
from sqlalchemy import select

from app.domain.entities.ticket import Ticket
from app.application.dtos.outbox_message import OutboxMessageDto
from app.infrastructure.database.models.outbox_event import OutboxEventModel
from app.infrastructure.database.models.ticket import TicketModel

@pytest.mark.asyncio
async def test_ticket_and_outbox_are_saved_in_same_transaction(
    test_session, uow
):
    ticket_id = uuid4()
    event_id = uuid4()

    ticket = Ticket(
        id=ticket_id,
        event_id=event_id,
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@example.com",
        seat="A15",
    )

    message = OutboxMessageDto(
        event_type="ticket_registered",
        payload={
            "ticket_id": str(ticket_id),
            "event_id": str(event_id),
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivan@example.com",
            "seat": "A15",
        },
    )

    async with uow:
        await uow.ticket_repository.save(ticket)
        await uow.outbox_repository.save(message)

    ticket_result = await test_session.get(TicketModel, ticket_id)

    result = await test_session.execute(
        select(OutboxEventModel).where(
            OutboxEventModel.event_type == "ticket_registered"
        )
    )
    outbox_event = result.scalar_one()

    assert ticket_result is not None
    assert ticket_result.id == ticket_id
    assert ticket_result.event_id == event_id

    assert outbox_event.event_type == "ticket_registered"
    assert outbox_event.payload["ticket_id"] == str(ticket_id)
    assert outbox_event.status == "pending"

@pytest.mark.asyncio
async def test_ticket_and_outbox_are_rolled_back_together(
    uow,
    test_session,
):
    ticket_id = uuid4()
    event_id = uuid4()

    ticket = Ticket(
        id=ticket_id,
        event_id=event_id,
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@example.com",
        seat="A15",
    )

    message = OutboxMessageDto(
        event_type="ticket_registered",
        payload={
            "ticket_id": str(ticket_id),
            "event_id": str(event_id),
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivan@example.com",
            "seat": "A15",
        },
    )
    
    with pytest.raises(RuntimeError, match="something went wrong"):
        async with uow:
            await uow.ticket_repository.save(ticket)
            await uow.outbox_repository.save(message)

            raise RuntimeError("something went wrong")

    ticket_result = await test_session.get(TicketModel, ticket_id)

    result = await test_session.execute(
        select(OutboxEventModel).where(
            OutboxEventModel.event_type == "ticket_registered"
        )
    )
    outbox_event = result.scalar_one_or_none()

    assert ticket_result is None
    assert outbox_event is None
