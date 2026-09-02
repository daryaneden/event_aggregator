from uuid import uuid4

import pytest

from app.application.exceptions import EventNotFoundException


@pytest.mark.asyncio
async def test_get_available_seats_returns_seats(client,
                                                 get_available_seats_use_case):
    event_id = uuid4()
    seats = ['A1', 'A2', 'B1']

    get_available_seats_use_case.execute.return_value = seats

    response = await client.get(f'/api/events/{event_id}/seats')

    assert response.status_code == 200
    assert response.json() == {'event_id': str(event_id),
                               'available_seats': seats}

    get_available_seats_use_case.execute.assert_awaited_once_with(event_id)

@pytest.mark.asyncio
async def test_get_available_seats_returns_404_when_event_not_found(client,
                                                                    get_available_seats_use_case):
    event_id = uuid4()

    get_available_seats_use_case.execute.side_effect = EventNotFoundException(event_id)

    response = await client.get(f'/api/events/{event_id}/seats')

    assert response.status_code == 404
    assert response.json()['detail'] == str(EventNotFoundException(event_id))

    get_available_seats_use_case.execute.assert_awaited_once_with(event_id)