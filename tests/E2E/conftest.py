import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from unittest.mock import AsyncMock

from app.main import app
from app.presentation.dependencies import (
    get_cancel_ticket_use_case,
    get_create_ticket_use_case,
    get_get_available_seats_use_case,
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


@pytest_asyncio.fixture
async def client(
    cancel_ticket_use_case,
    create_ticket_use_case,
    get_available_seats_use_case,
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

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()