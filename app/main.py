from fastapi import FastAPI

from app.presentation.routers.health_check import router as health_check_router
from app.presentation.routers.sync import router as sync_router
from app.presentation.routers.get_events import router as events_router
from app.presentation.routers.get_event import router as event_router

app = FastAPI()

app.include_router(health_check_router)
app.include_router(sync_router)
app.include_router(events_router)
app.include_router(event_router)