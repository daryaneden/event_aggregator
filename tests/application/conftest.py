from unittest.mock import AsyncMock, Mock

import pytest

@pytest.fixture
def provider():
    provider = Mock()
    provider.register_ticket = AsyncMock()
    provider.cancel_ticket = AsyncMock()
    provider.get_available_seats = AsyncMock()
    return provider


@pytest.fixture
def ticket_registry():
    registry = Mock()
    registry.get_event_id = Mock()
    registry.add = Mock()
    registry.remove = Mock()
    return registry


@pytest.fixture
def event_repository():
    repository = Mock()
    repository.get_by_id = AsyncMock()
    repository.get_events = AsyncMock()
    repository.save = AsyncMock()
    return repository


@pytest.fixture
def seats_cache():
    cache = Mock()
    cache.get = Mock()
    cache.set = Mock()
    return cache

@pytest.fixture
def sync_state_repository():
    repository = Mock()
    repository.get = AsyncMock()
    repository.save = AsyncMock()
    return repository


@pytest.fixture
def unit_of_work(sync_state_repository, event_repository):
    uow = AsyncMock()
    uow.sync_state_repository = sync_state_repository
    uow.event_repository = event_repository
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = None
    return uow

@pytest.fixture
def uow_factory(unit_of_work):
    factory = Mock(return_value=unit_of_work)
    return factory