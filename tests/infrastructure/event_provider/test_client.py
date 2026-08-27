from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID
import pytest
import httpx

from app.infrastructure.event_provider.events_provider_client import EventsProviderClient

@pytest.mark.asyncio
async def test_get_events_page_returns_events_page():
    response = Mock()

    response.json.return_value = {
        "results": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Concert",
                "place": {
                    "id": "650e8400-e29b-41d4-a716-446655440000",
                    "name": "Arena",
                    "city": "Helsinki",
                    "address": "Main street 1",
                    "seats_pattern": "pattern",
                    "changed_at": "2026-08-20T10:00:00",
                    "created_at": "2026-08-01T10:00:00",
                },
                "event_time": "2026-09-01T18:00:00",
                "registration_deadline": "2026-08-30T18:00:00",
                "status": "active",
                "number_of_visitors": 100,
                "changed_at": "2026-08-20T10:00:00",
                "created_at": "2026-08-01T10:00:00",
                "status_changed_at": "2026-08-20T10:00:00",
            }
        ],
        "next": "/api/events/?cursor=abc",
    }

    client = Mock()
    client.get = AsyncMock(return_value=response)

    provider = EventsProviderClient(client)

    changed_at = datetime(2026, 8, 20)

    result = await provider.get_events_page(
        changed_at=changed_at,
    )

    client.get.assert_awaited_once_with(
        "/api/events/?changed_at=2026-08-20"
    )

    response.raise_for_status.assert_called_once()

    assert len(result.events) == 1

    event = result.events[0]

    assert event.id == UUID(
        "550e8400-e29b-41d4-a716-446655440000"
    )
    assert event.name == "Concert"

    assert event.place.id == UUID(
        "650e8400-e29b-41d4-a716-446655440000"
    )
    assert event.place.name == "Arena"
    assert event.place.city == "Helsinki"
    assert event.place.address == "Main street 1"
    assert event.place.seats_pattern == "pattern"

    assert result.next_url == "/api/events/?cursor=abc"


@pytest.mark.asyncio
async def test_get_events_page_uses_provided_url():
    response = Mock()

    response.json.return_value = {
        "results": [],
        "next": None,
    }

    client = Mock()
    client.get = AsyncMock(return_value=response)

    provider = EventsProviderClient(client)

    changed_at = datetime(2026, 8, 20)
    url = "/api/events/?cursor=abc"

    await provider.get_events_page(
        changed_at=changed_at,
        url=url,
    )

    client.get.assert_awaited_once_with(url)

@pytest.mark.asyncio
async def test_get_events_page_raises_http_error():
    response = Mock()

    request = httpx.Request(
        "GET",
        "https://example.com/api/events/",
    )

    http_error = httpx.HTTPStatusError(
        "500 Internal Server Error",
        request=request,
        response=Mock(status_code=500),
    )

    response.raise_for_status.side_effect = http_error

    client = Mock()
    client.get = AsyncMock(return_value=response)

    provider = EventsProviderClient(client)

    with pytest.raises(httpx.HTTPStatusError):
        await provider.get_events_page(
            changed_at=datetime(2026, 8, 20),
        )