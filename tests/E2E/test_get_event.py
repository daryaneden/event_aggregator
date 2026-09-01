from datetime import datetime
from uuid import uuid4

import pytest

from app.application.exceptions import EventNotFoundException
from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.presentation.schemas.event_response import EventResponse
from app.presentation.schemas.place_response import PlaceResponse


@pytest.mark.asyncio
async def test_get_event_returns_event(
    client,
    get_event_use_case,
    event_response_mapper,
):
    event_id = uuid4()
    place_id = uuid4()

    place = Place(
        id=place_id,
        name="Conference Hall",
        city="Helsinki",
        address="Mannerheimintie 1",
        seats_pattern="AAAA",
    )

    event = Event(
        id=event_id,
        name="Python Conference",
        place=place,
        event_time=datetime(2026, 9, 10, 18, 0),
        registration_deadline=datetime(2026, 9, 9, 18, 0),
        status="active",
        number_of_visitors=100,
        changed_at=datetime(2026, 8, 20, 10, 0),
        created_at=datetime(2026, 8, 1, 10, 0),
        status_changed_at=datetime(2026, 8, 20, 10, 0),
    )

    expected_response = EventResponse(
        id=event_id,
        name="Python Conference",
        place=PlaceResponse(
            id=place_id,
            name="Conference Hall",
            city="Helsinki",
            address="Mannerheimintie 1",
            seats_pattern="AAAA",
        ),
        event_time=datetime(2026, 9, 10, 18, 0),
        registration_deadline=datetime(2026, 9, 9, 18, 0),
        status="active",
        number_of_visitors=100,
    )

    get_event_use_case.execute.return_value = event
    event_response_mapper.to_response.return_value = expected_response

    response = await client.get(f"/api/events/{event_id}")

    assert response.status_code == 200
    assert response.json() == expected_response.model_dump(mode="json")

    get_event_use_case.execute.assert_awaited_once_with(event_id)
    event_response_mapper.to_response.assert_called_once_with(event)


@pytest.mark.asyncio
async def test_get_event_returns_404_when_event_not_found(
    client,
    get_event_use_case,
):
    event_id = uuid4()

    get_event_use_case.execute.side_effect = EventNotFoundException(
        event_id
    )

    response = await client.get(f"/api/events/{event_id}")

    assert response.status_code == 404
    assert response.json() == {
        'detail': f'Event {event_id} is not found'
    }

    get_event_use_case.execute.assert_awaited_once_with(event_id)