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
