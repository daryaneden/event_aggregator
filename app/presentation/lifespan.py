from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from app.presentation.dependencies import build_sync_events_use_case_for_lifespan
from app.infrastructure.sync_worker import sync_worker

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