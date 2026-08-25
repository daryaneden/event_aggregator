from app.infrastructure.event_provider.events_provider_client import EventsProviderClient
from app.infrastructure.http.client import create_event_provider_client
from app.infrastructure.database.database import get_db_session
from httpx import AsyncClient
from fastapi import Depends
from typing import Annotated

async def get_events_provider_client(client: Annotated[AsyncClient, Depends(create_event_provider_client)]):
    return EventsProviderClient(client)