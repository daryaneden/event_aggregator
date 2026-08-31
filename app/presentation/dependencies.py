from app.infrastructure.event_provider.events_provider_client import EventsProviderClient
from app.infrastructure.database.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.database.repositories.sqlalchemy_sync_state_repository import SqlAlchemySyncStateRepository
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.infrastructure.uow.sqlalchemy_uow_factory import SqlAlchemyUnitOfWorkFactory
from app.infrastructure.http.client import create_event_provider_client
from app.infrastructure.database.database import get_db_session
from app.infrastructure.database.database import AsyncSessionFactory
from app.application.use_cases.get_events import GetEventsUseCase
from app.application.use_cases.get_event import GetEventUseCase
from app.application.use_cases.sync_events import SyncEventsUseCase
from app.application.use_cases.register_ticket_use_case import RegisterTicketUseCase
from app.presentation.mappers.event_response_mapper import EventResponseMapper
from app.infrastructure.uow.sqlalchemy_background_uow import SqlAlchemyBackgroundUnitOfWork
from app.config.setting import Settings
from app.application.use_cases.get_available_seats import GetAvailableSeatsUseCase
from app.infrastructure.cache.in_memory_seats_cache import InMemorySeatsCache

from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from fastapi import Depends
from typing import Annotated

def get_settings():
    return Settings()

def get_async_session_factory():
    return AsyncSessionFactory

async def get_events_provider_client(client: Annotated[AsyncClient, Depends(create_event_provider_client)],
                                     settings: Annotated[Settings, Depends(get_settings)]):
    return EventsProviderClient(client, base_url=settings.EVENT_PROVIDER_URL)

async def get_sqlalchemy_event_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return SqlAlchemyEventRepository(session)

async def get_sqlalchemy_sync_state_repository(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return SqlAlchemySyncStateRepository(session)

async def get_get_events_use_case(event_repository: Annotated[SqlAlchemyEventRepository, Depends(get_sqlalchemy_event_repository)]):
    return GetEventsUseCase(event_repository)

async def get_event_response_mapper():
    return EventResponseMapper()

async def get_get_event_use_case(event_repository: Annotated[SqlAlchemyEventRepository, Depends(get_sqlalchemy_event_repository)]):
    return GetEventUseCase(event_repository)

def get_uow_factory() -> SqlAlchemyUnitOfWorkFactory:
    return SqlAlchemyUnitOfWorkFactory(
        session_factory=AsyncSessionFactory,
        uow_builder=build_uow
    )

async def get_sync_events_use_case(provider: Annotated[EventsProviderClient, Depends(get_events_provider_client)],
                                   uow_factory: Annotated[
        SqlAlchemyUnitOfWorkFactory,
        Depends(get_uow_factory),
    ]):

    print(">>> uow_factory:", type(uow_factory))

    uow = uow_factory()

    print(">>> uow:", type(uow))
    print(">>> has __aenter__:", hasattr(uow, "__aenter__"))
    print(">>> has __aexit__:", hasattr(uow, "__aexit__"))

    return SyncEventsUseCase(provider, uow_factory)

async def get_background_sqlalchemy_unit_of_work(event_repository: Annotated[SqlAlchemyEventRepository, Depends(get_sqlalchemy_event_repository)],
                                                 sync_state_repository: Annotated[SqlAlchemySyncStateRepository, Depends(get_sqlalchemy_sync_state_repository)],
                                                 factory=AsyncSessionFactory,
                                                 ):
    return SqlAlchemyBackgroundUnitOfWork(factory, event_repository, sync_state_repository)

def build_uow(session: AsyncSession) -> SqlAlchemyUnitOfWork:
    event_repository = SqlAlchemyEventRepository(session)
    sync_state_repository = SqlAlchemySyncStateRepository(session)

    return SqlAlchemyUnitOfWork(
        session=session,
        event_repository=event_repository,
        sync_state_repository=sync_state_repository,
    )
seats_cache = InMemorySeatsCache()

async def get_available_seats_use_case(provider: Annotated[EventsProviderClient, Depends(get_events_provider_client)]) -> GetAvailableSeatsUseCase:
    return GetAvailableSeatsUseCase(
        provider=provider,
        cache=seats_cache,
    )

async def get_register_ticket_use_case(provider: Annotated[EventsProviderClient, Depends(get_events_provider_client)]):
    return RegisterTicketUseCase(provider)

#lifespan dependencies 

def build_events_provider_client_for_lifespan() -> EventsProviderClient:
    client = create_event_provider_client()
    settings = get_settings()

    return EventsProviderClient(
        client,
        base_url=settings.EVENT_PROVIDER_URL
    )

def build_sync_events_use_case_for_lifespan() -> SyncEventsUseCase:
    return SyncEventsUseCase(
        provider=build_events_provider_client_for_lifespan(),
        uow_factory=get_uow_factory()
    )