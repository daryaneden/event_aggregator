from uuid import uuid4

import pytest

from app.application.exceptions import TicketNotFoundException


@pytest.mark.asyncio
async def test_cancel_ticket_returns_success(client,
                                             cancel_ticket_use_case):
    ticket_id = uuid4()

    response = await client.delete(f"/api/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json() == {"success": True}

    cancel_ticket_use_case.execute.assert_awaited_once_with(ticket_id)

@pytest.mark.asyncio
async def test_cancel_ticket_returns_404_when_ticket_not_found(client,
                                                               cancel_ticket_use_case):
    ticket_id = uuid4()

    cancel_ticket_use_case.execute.side_effect = TicketNotFoundException(ticket_id)

    response = await client.delete(f"/api/tickets/{ticket_id}")

    assert response.status_code == 404
    assert response.json()["detail"]

    cancel_ticket_use_case.execute.assert_awaited_once_with(ticket_id)