from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infrastructure.database.database import Base

from app.infrastructure.event_provider.events_provider_client import EventsProviderClient
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository
from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio

@pytest.fixture
def http_client():
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.fixture
def base_url():
    return "https://example.com"


@pytest.fixture
def http_response():
    response = Mock()
    response.raise_for_status = Mock()
    return response

@pytest.fixture
def events_provider(http_client, base_url):
    return EventsProviderClient(
        client=http_client,
        base_url=base_url,
    )


@pytest.fixture
def provider_event():
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Concert",
        "place": {
            "id": "650e8400-e29b-41d4-a716-446655440000",
            "name": "Arena",
            "city": "Helsinki",
            "address": "Main street 1",
            "seats_pattern": "pattern",
            "changed_at": "2026-08-20T10:00:00",
            "created_at": "2026-08-01T10:00:00",
        },
        "event_time": "2026-09-01T18:00:00",
        "registration_deadline": "2026-08-30T18:00:00",
        "status": "active",
        "number_of_visitors": 100,
        "changed_at": "2026-08-20T10:00:00",
        "created_at": "2026-08-01T10:00:00",
        "status_changed_at": "2026-08-20T10:00:00",
    }

@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(
        url='postgresql+asyncpg://postgres:password@localhost:5432/student_daryaneden-events-aggregator-postgres-test',
                             future=True,\
                             echo=True,
                             pool_pre_ping=True
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def test_session(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(
        test_engine,
                                            autoflush=False, 
                                            expire_on_commit=False
        )
    async with async_session() as session:
        yield session
        await session.rollback()
    

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def event_repository(test_session):
    return SqlAlchemyEventRepository(test_session)


@pytest.fixture
def sync_state_repository(test_session):
    return SqlAlchemySyncStateRepository(test_session)