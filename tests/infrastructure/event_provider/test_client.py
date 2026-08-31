from datetime import datetime
from unittest.mock import AsyncMock, Mock
import pytest
import httpx
from uuid import UUID

from app.infrastructure.event_provider.events_provider_client import EventsProviderClient

@pytest.mark.asyncio
async def test_get_events_page_returns_events_page(
    events_provider,
    http_client,
    http_response,
    provider_event,
):
    http_response.json.return_value = {
        "results": [provider_event],
        "next": None,
    }

    http_client.get.return_value = http_response

    result = await events_provider.get_events_page(
    changed_at=datetime(2000, 1, 1))

    assert len(result.events) == 1
    assert result.events[0].id == UUID(provider_event["id"])
    assert result.events[0].name == provider_event["name"]
    assert result.next_url is None

    http_client.get.assert_awaited_once_with(
        "/api/events/?changed_at=2000-01-01"
    )

    http_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_get_events_page_uses_provided_url():
    response = Mock()

    response.json.return_value = {
        "results": [],
        "next": None,
    }

    client = Mock()
    client.get = AsyncMock(return_value=response)

    provider = EventsProviderClient(
    client=client,
    base_url="https://example.com",
)

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

    provider = EventsProviderClient(
    client=client,
    base_url="https://example.com",
)

    with pytest.raises(httpx.HTTPStatusError):
        await provider.get_events_page(
            changed_at=datetime(2026, 8, 20),
        )