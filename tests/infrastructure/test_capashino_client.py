from unittest.mock import AsyncMock, Mock

import pytest

from app.infrastructure.capashino import CapashinoClient


@pytest.mark.asyncio
async def test_send_notification():
    response = Mock()

    client = Mock()
    client.post = AsyncMock(return_value=response)

    notification_client = CapashinoClient(client=client)

    await notification_client.send_notification(message='Вы успешно зарегистрированы на мероприятие',
                                                reference_id='ticket-123',
                                                idempotency_key='message-123')

    client.post.assert_awaited_once_with('/api/notifications',
                                         json={'message': 'Вы успешно зарегистрированы на мероприятие',
                                               'reference_id': 'ticket-123',
                                               'idempotency_key': 'message-123'})

    response.raise_for_status.assert_called_once()