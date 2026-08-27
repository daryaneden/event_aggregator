from app.infrastructure.event_provider.events_provider_client import EventsProviderClient
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.infrastructure.http.client import create_event_provider_client
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.database import AsyncSessionFactory
from app.application.use_cases.get_events import GetEventsUseCase
from app.application.use_cases.get_event import GetEventUseCase
from app.presentation.mappers.event_response_mapper import EventResponseMapper
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from fastapi import Depends
from typing import Annotated

def get_async_session_factory():
    return AsyncSessionFactory

async def get_events_provider_client(client: Annotated[AsyncClient, Depends(create_event_provider_client)]):
    return EventsProviderClient(client)

async def get_sqlalchemy_event_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return SqlAlchemyEventRepository(session)

async def get_sqlalchemy_sync_state_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return SqlAlchemySyncStateRepository(session)

async def get_sqlalchemy_unit_of_work(session: Annotated[AsyncSession, Depends(get_db_session)],
                                      event_repository: Annotated[SqlAlchemyEventRepository, Depends(get_sqlalchemy_event_repository)],
                                      sync_state_repository: Annotated[SqlAlchemySyncStateRepository, Depends(get_sqlalchemy_sync_state_repository)]):
    return SqlAlchemyUnitOfWork(session, event_repository, sync_state_repository)

async def get_get_events_use_case(event_repository: Annotated[SqlAlchemyEventRepository, Depends(get_sqlalchemy_event_repository)]):
    return GetEventsUseCase(event_repository)

async def get_event_response_mapper():
    return EventResponseMapper()

def get_get_event_use_case(event_repository: Annotated[SqlAlchemyEventRepository, Depends(get_sqlalchemy_event_repository)]):
    return GetEventUseCase(event_repository)