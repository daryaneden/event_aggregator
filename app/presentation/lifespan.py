import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.sync_worker import sync_worker
from app.presentation.dependencies import build_sync_events_use_case_for_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    use_case = build_sync_events_use_case_for_lifespan()
    task = asyncio.create_task(sync_worker(use_case))

    yield

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass