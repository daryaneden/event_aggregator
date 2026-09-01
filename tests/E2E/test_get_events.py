from datetime import datetime
from uuid import uuid4

import pytest

from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.presentation.schemas.event_response import EventResponse
from app.presentation.schemas.event_list_response import EventListResponse
from app.presentation.schemas.place_response import PlaceResponse


@pytest.mark.asyncio
async def test_get_events_returns_events(
    client,
    get_events_use_case,
    event_response_mapper,
):
    place = Place(
        id=uuid4(),
        name="Conference Hall",
        city="Helsinki",
        address="Mannerheimintie 1",
        seats_pattern="AAAA",
    )

    event = Event(
        id=uuid4(),
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

    events = [event]
    total = 1

    expected_response = EventListResponse(
        count=1,
        next=None,
        previous=None,
        results=[
            EventResponse(
                id=event.id,
                name=event.name,
                place=PlaceResponse(
                    id=place.id,
                    name=place.name,
                    city=place.city,
                    address=place.address,
                    seats_pattern=place.seats_pattern,
                ),
                event_time=event.event_time,
                registration_deadline=event.registration_deadline,
                status=event.status,
                number_of_visitors=event.number_of_visitors,
            )
        ],
    )

    get_events_use_case.execute.return_value = (
        events,
        total,
    )

    event_response_mapper.to_list_response.return_value = expected_response

    response = await client.get(
        "/api/events",
        params={
            "page": 1,
            "page_size": 10,
        },
    )

    assert response.status_code == 200

    assert response.json() == expected_response.model_dump(mode="json")

    get_events_use_case.execute.assert_awaited_once_with(
        date_from=None,
        page=1,
        page_size=10,
    )

    event_response_mapper.to_list_response.assert_called_once_with(
        events=events,
        total=total,
        page=1,
        page_size=10,
    )