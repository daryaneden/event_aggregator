from unittest.mock import Mock
from uuid import UUID

import pytest

from app.application.use_cases.get_event import GetEventUseCase
from app.application.exceptions import EventNotFoundException


@pytest.mark.asyncio
async def test_get_event_returns_event(event_repository):

    event_id = UUID('550e8400-e29b-41d4-a716-446655440000')
    event = Mock()

    event_repository.get_by_id.return_value = event

    use_case = GetEventUseCase(event_repository=event_repository)

    result = await use_case.execute(event_id)

    assert result is event

    event_repository.get_by_id.assert_awaited_once_with(event_id)

@pytest.mark.asyncio
async def test_get_event_raises_exception_when_event_not_found(event_repository):
    event_id = UUID('550e8400-e29b-41d4-a716-446655440000')

    event_repository.get_by_id.return_value = None

    use_case = GetEventUseCase(event_repository=event_repository)

    with pytest.raises(EventNotFoundException):
        await use_case.execute(event_id)