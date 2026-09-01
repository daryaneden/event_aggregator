import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock, Mock

from app.main import app
from app.presentation.dependencies import (
    get_cancel_ticket_use_case,
    get_create_ticket_use_case,
    get_get_available_seats_use_case,
    get_get_event_use_case,
    get_event_response_mapper,
    get_sync_events_use_case
)


@pytest.fixture
def cancel_ticket_use_case():
    return AsyncMock()


@pytest.fixture
def create_ticket_use_case():
    return AsyncMock()


@pytest.fixture
def get_available_seats_use_case():
    return AsyncMock()

@pytest.fixture
def get_event_use_case():
    return AsyncMock()


@pytest.fixture
def event_response_mapper():
    return Mock()

@pytest.fixture
def sync_events_use_case():
    return AsyncMock()

@pytest_asyncio.fixture
async def client(
    cancel_ticket_use_case,
    create_ticket_use_case,
    get_available_seats_use_case,
    get_event_use_case,
    event_response_mapper,
    sync_events_use_case
):
    app.dependency_overrides[get_cancel_ticket_use_case] = (
        lambda: cancel_ticket_use_case
    )
    app.dependency_overrides[get_create_ticket_use_case] = (
        lambda: create_ticket_use_case
    )
    app.dependency_overrides[get_get_available_seats_use_case] = (
        lambda: get_available_seats_use_case
    )

    app.dependency_overrides[get_get_event_use_case] = (
        lambda: get_event_use_case
    )

    app.dependency_overrides[get_event_response_mapper] = (
        lambda: event_response_mapper
    )

    app.dependency_overrides[get_sync_events_use_case] = (
    lambda: sync_events_use_case
)

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()