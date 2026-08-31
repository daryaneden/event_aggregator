from datetime import datetime
from unittest.mock import AsyncMock, Mock
import pytest
from uuid import uuid4
import inspect

from app.application.dtos.events_page import EventsPage
from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.infrastructure.event_provider.events_paginator import EventsPaginator

print(inspect.signature(Event))

def create_event(name: str) -> Event:
    return Event(
        id=uuid4(),
        name=name,
        place=Place(
            id=uuid4(),
            name="Arena",
            city="Helsinki",
            address="Main street 1",
            seats_pattern="pattern"
        ),
        event_time=datetime(2026, 9, 1, 18, 0),
        registration_deadline=datetime(2026, 8, 30, 18, 0),
        status="active",
        number_of_visitors=100,
        changed_at=datetime(2026, 8, 20, 10, 0),
        created_at=datetime(2026, 8, 1, 10, 0),
        status_changed_at=datetime(2026, 8, 20, 10, 0),
        )

@pytest.mark.asyncio
async def test_paginator_returns_events_from_one_page():
    event_1 = create_event("Concert")
    event_2 = create_event("Theatre")

    page = EventsPage(
        events=[event_1, event_2],
        next_url=None,
    )

    provider = Mock()
    provider.get_events_page = AsyncMock(
        return_value=page,
    )

    changed_at = datetime(2026, 8, 20)

    paginator = EventsPaginator(
        provider=provider,
        changed_at=changed_at,
    )

    events = [
        event
        async for event in paginator
    ]

    assert events == [event_1, event_2]

    provider.get_events_page.assert_awaited_once_with(
        changed_at=changed_at,
        url=None,
    )


@pytest.mark.asyncio
async def test_paginator_iterates_over_multiple_pages():
    event_1 = create_event("Concert")
    event_2 = create_event("Theatre")
    event_3 = create_event("Exhibition")

    first_page = EventsPage(
        events=[event_1, event_2],
        next_url="/api/events/?cursor=abc",
    )

    second_page = EventsPage(
        events=[event_3],
        next_url=None,
    )

    provider = Mock()

    provider.get_events_page = AsyncMock(
        side_effect=[
            first_page,
            second_page,
        ],
    )

    changed_at = datetime(2026, 8, 20)

    paginator = EventsPaginator(
        provider=provider,
        changed_at=changed_at,
    )

    events = [
        event
        async for event in paginator
    ]

    assert events == [
        event_1,
        event_2,
        event_3,
    ]

    assert provider.get_events_page.await_count == 2

    provider.get_events_page.assert_any_await(
        changed_at=changed_at,
        url=None,
    )

    provider.get_events_page.assert_any_await(
        changed_at=changed_at,
        url="/api/events/?cursor=abc",
    )


@pytest.mark.asyncio
async def test_paginator_returns_empty_result_for_empty_page():
    page = EventsPage(
        events=[],
        next_url=None,
    )

    provider = Mock()

    provider.get_events_page = AsyncMock(
        return_value=page,
    )

    changed_at = datetime(2026, 8, 20)

    paginator = EventsPaginator(
        provider=provider,
        changed_at=changed_at,
    )

    events = [
        event
        async for event in paginator
    ]

    assert events == []

    provider.get_events_page.assert_awaited_once_with(
        changed_at=changed_at,
        url=None,
    )