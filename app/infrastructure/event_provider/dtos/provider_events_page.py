from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from app.infrastructure.event_provider.dtos.provider_event import ProviderEventDTO

class ProviderEventsPageDTO(BaseModel):
    results: list[ProviderEventDTO]
    next: str | None