from datetime import date, datetime
from uuid import uuid4

import pytest

from app.domain.entities.event import Event
from app.domain.entities.place import Place


@pytest.mark.asyncio
async def test_save_and_get_by_id(
    event_repository,
    test_session,
):
    event_id = uuid4()
    place_id = uuid4()

    event = Event(
        id=event_id,
        name="Concert",
        place=Place(
            id=place_id,
            name="Arena",
            city="Helsinki",
            address="Main street 1",
            seats_pattern="pattern",
        ),
        event_time=datetime(2026, 9, 1, 18, 0),
        registration_deadline=datetime(2026, 8, 30, 18, 0),
        status="active",
        number_of_visitors=100,
        changed_at=datetime(2026, 8, 20, 10, 0),
        created_at=datetime(2026, 8, 1, 10, 0),
        status_changed_at=datetime(2026, 8, 20, 10, 0),
    )

    await event_repository.save(event)
    await test_session.commit()

    result = await event_repository.get_by_id(event_id)

    assert result is not None
    assert result.id == event_id
    assert result.name == "Concert"
    assert result.place.id == place_id
    assert result.place.city == "Helsinki"


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_missing_event(
    event_repository,
):
    result = await event_repository.get_by_id(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_get_events_returns_filtered_and_paginated_events(
    event_repository,
    test_session,
):
    event_1 = Event(
        id=uuid4(),
        name="Concert",
        place=Place(
            id=uuid4(),
            name="Arena",
            city="Helsinki",
            address="Main street 1",
            seats_pattern="pattern",
        ),
        event_time=datetime(2026, 9, 1, 18, 0),
        registration_deadline=datetime(2026, 8, 30, 18, 0),
        status="active",
        number_of_visitors=100,
        changed_at=datetime(2026, 8, 20, 10, 0),
        created_at=datetime(2026, 8, 1, 10, 0),
        status_changed_at=datetime(2026, 8, 20, 10, 0),
    )

    event_2 = Event(
        id=uuid4(),
        name="Conference",
        place=Place(
            id=uuid4(),
            name="Hall",
            city="Helsinki",
            address="Second street 2",
            seats_pattern="pattern",
        ),
        event_time=datetime(2026, 9, 10, 18, 0),
        registration_deadline=datetime(2026, 9, 8, 18, 0),
        status="active",
        number_of_visitors=50,
        changed_at=datetime(2026, 8, 21, 10, 0),
        created_at=datetime(2026, 8, 2, 10, 0),
        status_changed_at=datetime(2026, 8, 21, 10, 0),
    )

    event_3 = Event(
        id=uuid4(),
        name="Old Event",
        place=Place(
            id=uuid4(),
            name="Old Hall",
            city="Helsinki",
            address="Old street 3",
            seats_pattern="pattern",
        ),
        event_time=datetime(2026, 8, 1, 18, 0),
        registration_deadline=datetime(2026, 7, 30, 18, 0),
        status="finished",
        number_of_visitors=30,
        changed_at=datetime(2026, 8, 1, 10, 0),
        created_at=datetime(2026, 7, 1, 10, 0),
        status_changed_at=datetime(2026, 8, 1, 10, 0),
    )

    await event_repository.save(event_1)
    await event_repository.save(event_2)
    await event_repository.save(event_3)

    await test_session.commit()

    events, total = await event_repository.get_events(
        date_from=date(2026, 9, 1),
        page=2,
        page_size=1,
    )

    assert total == 2
    assert len(events) == 1
    assert events[0].name == "Conference"
    assert events[0].event_time == datetime(2026, 9, 10, 18, 0)
