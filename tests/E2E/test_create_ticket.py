from uuid import uuid4

import pytest

from app.application.dtos.register_ticket import RegisterTicketDTO


@pytest.mark.asyncio
async def test_register_ticket_returns_ticket_id(client,
                                                 create_ticket_use_case):
    event_id = uuid4()
    ticket_id = uuid4()

    create_ticket_use_case.execute.return_value = ticket_id

    payload = { "event_id": str(event_id),
               "first_name": "Anna",
               "last_name": "Smith",
               "email": "anna@example.com",
               "seat": "A12"}

    response = await client.post("/api/tickets",
                                 json=payload)

    assert response.status_code == 201
    assert response.json() == {"ticket_id": str(ticket_id)}

    create_ticket_use_case.execute.assert_awaited_once_with(RegisterTicketDTO(event_id=event_id,
                                                                              first_name="Anna",
                                                                              last_name="Smith",
                                                                              email="anna@example.com",
                                                                              seat="A12"))