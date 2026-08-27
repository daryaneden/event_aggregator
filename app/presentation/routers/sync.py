from fastapi import APIRouter

from app.infrastructure.celery.task import sync_events

router = APIRouter(
    prefix="/api/sync",
    tags=["sync"],
)


@router.post("/trigger", status_code=200)
async def trigger_sync():
    sync_events.delay()

    return {
        "message": "Synchronization started"
    }