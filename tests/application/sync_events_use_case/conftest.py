from unittest.mock import AsyncMock, Mock
import pytest

@pytest.fixture
def uow():
    sync_state_repository = AsyncMock()
    event_repository = AsyncMock()

    uow = AsyncMock()

    uow.sync_state_repository = sync_state_repository
    uow.event_repository = event_repository

    uow.__aenter__.return_value = uow

    return uow

@pytest.fixture
def uow_factory(uow):
    return Mock(return_value=uow)