from uuid import UUID

import pytest
from unittest.mock import AsyncMock

from app.application.use_cases.get_available_seats import GetAvailableSeatsUseCase
from app.application.exceptions import EventNotFoundException

@pytest.mark.asyncio
async def test_get_available_seats_returns_cached_seats(
    provider,
    seats_cache,
):
    event_id = UUID("550e8400-e29b-41d4-a716-446655440000")
    seats = ["A1", "A2", "A3"]

    seats_cache.get.return_value = seats

    use_case = GetAvailableSeatsUseCase(
        provider=provider,
        cache=seats_cache,
    )

    result = await use_case.execute(event_id)

    assert result == seats

    seats_cache.get.assert_called_once_with(event_id)
    provider.get_available_seats.assert_not_called()

@pytest.mark.asyncio
async def test_get_available_seats_loads_from_provider_and_caches(
    provider,
    seats_cache,
):
    event_id = UUID("550e8400-e29b-41d4-a716-446655440000")
    seats = ["A1", "A2", "A3"]

    seats_cache.get.return_value = None
    provider.get_available_seats = AsyncMock(return_value=seats)

    use_case = GetAvailableSeatsUseCase(
        provider=provider,
        cache=seats_cache,
    )

    result = await use_case.execute(event_id)

    assert result == seats

    seats_cache.get.assert_called_once_with(event_id)

    provider.get_available_seats.assert_awaited_once_with(event_id)

    seats_cache.set.assert_called_once_with(
        event_id,
        seats,
    )

@pytest.mark.asyncio
async def test_get_available_seats_raises_exception_when_event_not_found(
    provider,
    seats_cache,
):
    event_id = UUID("550e8400-e29b-41d4-a716-446655440000")

    seats_cache.get.return_value = None
    provider.get_available_seats = AsyncMock(return_value=None)

    use_case = GetAvailableSeatsUseCase(
        provider=provider,
        cache=seats_cache,
    )

    with pytest.raises(EventNotFoundException):
        await use_case.execute(event_id)

    seats_cache.set.assert_not_called()