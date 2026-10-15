import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.cache.in_memory_seats_cache import InMemorySeatsCache
from app.infrastructure.cache.metrics_seats_cache import MetricsSeatsCache
from app.infrastructure.outbox_worker import outbox_worker
from app.infrastructure.sync_worker import sync_worker
from app.presentation.dependencies import (
    build_process_outbox_use_case_for_lifespan,
    build_sync_events_use_case_for_lifespan,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cache = InMemorySeatsCache()
    app.state.seats_cache = MetricsSeatsCache(cache)

    sync_use_case = build_sync_events_use_case_for_lifespan()
    sync_task = asyncio.create_task(sync_worker(sync_use_case))

    outbox_use_case = build_process_outbox_use_case_for_lifespan()
    outbox_task = asyncio.create_task(outbox_worker(outbox_use_case))

    yield

    sync_task.cancel()
    outbox_task.cancel()

    try:
        await sync_task
    except asyncio.CancelledError:
        pass

    try:
        await outbox_task
    except asyncio.CancelledError:
        pass