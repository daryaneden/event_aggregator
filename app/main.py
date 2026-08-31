from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.presentation.routers.health_check import router as health_check_router
from app.presentation.routers.sync import router as sync_router
from app.presentation.routers.get_events import router as events_router
from app.presentation.routers.get_event import router as event_router
from app.presentation.routers.get_available_seats import router as available_seats_router
from app.presentation.routers.create_ticket import router as create_ticket_router
from app.presentation.routers.cancel_ticket import router as cancel_ticket_router
from app.presentation.lifespan import lifespan
from app.presentation.exception_handlers import validation_exception_handler

app = FastAPI(lifespan=lifespan)

app.include_router(health_check_router)
app.include_router(sync_router)
app.include_router(events_router)
app.include_router(event_router)
app.include_router(available_seats_router)
app.include_router(create_ticket_router)
app.include_router(cancel_ticket_router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)