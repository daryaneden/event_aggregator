from datetime import datetime
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