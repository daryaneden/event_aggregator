import asyncio

import httpx

from app.application.use_cases.sync_events import SyncEventsUseCase
from app.config.setting import Settings
from app.infrastructure.celery.app import celery_app
from app.infrastructure.event_provider.events_provider_client import EventsProviderClient
from app.infrastructure.celery.sqlalchemy_uow import SqlAlchemyCeleryUnitOfWork

settings = Settings()

async def run_sync_events() -> None:

    client = httpx.AsyncClient(
        base_url=settings.EVENT_PROVIDER_URL,
        headers={
            "x-api-key": settings.EVENT_PROVIDER_API_KEY,
        },
        follow_redirects=True,
    )

    try:
        provider = EventsProviderClient(
            client=client,
        )

        use_case = SyncEventsUseCase(
        provider=provider,
        uow_factory=SqlAlchemyCeleryUnitOfWork,
)

        await use_case.execute()

    finally:
        await client.aclose()


@celery_app.task
def sync_events() -> None:
    asyncio.run(
        run_sync_events()
    )