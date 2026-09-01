from pydantic import BaseModel

from app.infrastructure.event_provider.dtos.provider_event import ProviderEventDTO

class ProviderEventsPageDTO(BaseModel):
    results: list[ProviderEventDTO]
    next: str | None