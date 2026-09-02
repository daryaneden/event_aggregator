from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def http_client():
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.fixture
def base_url():
    return 'https://example.com'

@pytest.fixture
def provider_event():
    return {
        'id': '550e8400-e29b-41d4-a716-446655440000',
        'name': 'Concert',
        'place': {
            'id': '650e8400-e29b-41d4-a716-446655440000',
            'name': 'Arena',
            'city': 'Helsinki',
            'address': 'Main street 1',
            'seats_pattern': 'pattern',
            'changed_at': '2026-08-20T10:00:00',
            'created_at': '2026-08-01T10:00:00',
        },
        'event_time': '2026-09-01T18:00:00',
        'registration_deadline': '2026-08-30T18:00:00',
        'status': 'active',
        'number_of_visitors': 100,
        'changed_at': '2026-08-20T10:00:00',
        'created_at': '2026-08-01T10:00:00',
        'status_changed_at': '2026-08-20T10:00:00',
    }