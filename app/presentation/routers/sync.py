from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Annotated

from app.application.use_cases.sync_events import SyncEventsUseCase
from app.presentation.dependencies import get_sync_events_use_case

router = APIRouter(
    prefix="/api/sync",
    tags=["sync"],
)


@router.post("/trigger", status_code=202)
async def trigger_sync(
    background_tasks: BackgroundTasks,
    use_case: Annotated[
        SyncEventsUseCase,
        Depends(get_sync_events_use_case),
    ],
):
    background_tasks.add_task(use_case.execute)

    return {
        "message": "Synchronization started",
    }