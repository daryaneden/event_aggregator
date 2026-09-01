from datetime import date

import pytest

from app.application.use_cases.get_events import GetEventsUseCase

@pytest.mark.asyncio
async def test_get_events_returns_events_and_total(event_repository):

    events = ['event1', 'event2']
    total = 2

    date_from = date(2026, 8, 1)
    page = 2
    page_size = 10

    event_repository.get_events.return_value = (events, total)

    use_case = GetEventsUseCase(event_repository=event_repository)

    result = await use_case.execute(date_from=date_from,
                                    page=page,
                                    page_size=page_size)

    assert result == (events, total)

    event_repository.get_events.assert_awaited_once_with(date_from=date_from,
                                                         page=page,
                                                         page_size=page_size)