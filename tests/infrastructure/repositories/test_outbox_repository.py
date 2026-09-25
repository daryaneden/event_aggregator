from datetime import datetime
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from app.application.dtos.outbox_message import OutboxMessageDto
from app.domain.entities.ticket import Ticket
from app.infrastructure.database.models.event import EventModel
from app.infrastructure.database.models.outbox_event import OutboxEventModel
from app.infrastructure.database.models.place import PlaceModel
from app.infrastructure.database.models.ticket import TicketModel


async def create_event(test_session, provider_event):
    place_data = provider_event["place"]

    place = PlaceModel(
        id=UUID(place_data["id"]),
        name=place_data["name"],
        city=place_data["city"],
        address=place_data["address"],
        seats_pattern=place_data["seats_pattern"]
    )

    event = EventModel(
        id=UUID(provider_event["id"]),
        name=provider_event["name"],
        place_id=place.id,
        event_time=datetime.fromisoformat(provider_event["event_time"]),
        registration_deadline=datetime.fromisoformat(
            provider_event["registration_deadline"]
        ),
        status=provider_event["status"],
        number_of_visitors=provider_event["number_of_visitors"],
        changed_at=datetime.fromisoformat(provider_event["changed_at"]),
        created_at=datetime.fromisoformat(provider_event["created_at"]),
        status_changed_at=datetime.fromisoformat(
            provider_event["status_changed_at"]
        ),
    )

    test_session.add(place)
    test_session.add(event)

    await test_session.commit()


@pytest.mark.asyncio
async def test_ticket_and_outbox_are_saved_in_same_transaction(
    test_session,
    uow,
    provider_event,
):
    ticket_id = uuid4()
    event_id = UUID(provider_event["id"])

    await create_event(
        test_session=test_session,
        provider_event=provider_event,
    )

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

    ticket_result = await test_session.get(
        TicketModel,
        ticket_id,
    )

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
    assert outbox_event.payload["event_id"] == str(event_id)
    assert outbox_event.payload["first_name"] == "Ivan"
    assert outbox_event.payload["last_name"] == "Ivanov"
    assert outbox_event.payload["email"] == "ivan@example.com"
    assert outbox_event.payload["seat"] == "A15"
    assert outbox_event.status == "pending"


@pytest.mark.asyncio
async def test_ticket_and_outbox_are_rolled_back_together(
    uow,
    test_session,
    provider_event,
):
    ticket_id = uuid4()
    event_id = UUID(provider_event["id"])

    await create_event(
        test_session=test_session,
        provider_event=provider_event,
    )

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

    with pytest.raises(
        RuntimeError,
        match="something went wrong",
    ):
        async with uow:
            await uow.ticket_repository.save(ticket)
            await uow.outbox_repository.save(message)

            raise RuntimeError("something went wrong")

    ticket_result = await test_session.get(
        TicketModel,
        ticket_id,
    )

    result = await test_session.execute(
        select(OutboxEventModel).where(
            OutboxEventModel.event_type == "ticket_registered"
        )
    )
    outbox_event = result.scalar_one_or_none()

    assert ticket_result is None
    assert outbox_event is None
