from uuid import UUID
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.process_outbox import ProcessOutboxUseCase
from app.application.dtos.outbox_message import PendingOutboxMessage


@pytest.mark.asyncio
async def test_process_outbox_sends_notification_and_marks_as_sent(uow_factory,
                                                                   unit_of_work,
                                                                   notification_client):
    message_id = UUID('1fed0122-b675-42e2-8ae7-49bfb53e8d7f')
    ticket_id = UUID('550e8400-e29b-41d4-a716-446655440000')

    message = PendingOutboxMessage(id=message_id,
                                   event_type='ticket_registered',
                                   payload={'ticket_id': str(ticket_id)})

    unit_of_work.outbox_repository.get_pending = AsyncMock(return_value=[message])

    unit_of_work.outbox_repository.mark_as_sent = AsyncMock()

    notification_client.send_notification = AsyncMock()

    use_case = ProcessOutboxUseCase(uow_factory=uow_factory,
                                    notification_client=notification_client)

    await use_case.execute()

    notification_client.send_notification.assert_awaited_once_with(message='Вы успешно зарегистрированы на мероприятие',
                                                                   reference_id=str(ticket_id),
                                                                   idempotency_key=str(message_id))

    unit_of_work.outbox_repository.mark_as_sent.assert_awaited_once_with(message_id)


@pytest.mark.asyncio
async def test_process_outbox_does_not_mark_as_sent_if_notification_fails(uow_factory,
                                                                          unit_of_work,
                                                                          notification_client):

    message_id = UUID('1fed0122-b675-42e2-8ae7-49bfb53e8d7f')
    ticket_id = UUID('550e8400-e29b-41d4-a716-446655440000')

    message = PendingOutboxMessage(id=message_id,
                                   event_type='ticket_registered',
                                   payload={'ticket_id': str(ticket_id)})

    unit_of_work.outbox_repository.get_pending = AsyncMock(return_value=[message])

    unit_of_work.outbox_repository.mark_as_sent = AsyncMock()

    notification_client.send_notification = AsyncMock(side_effect=Exception('Capashino unavailable'))

    use_case = ProcessOutboxUseCase(uow_factory=uow_factory,
                                    notification_client=notification_client)

    await use_case.execute()

    notification_client.send_notification.assert_awaited_once()

    unit_of_work.outbox_repository.mark_as_sent.assert_not_awaited()