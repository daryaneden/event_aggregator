from httpx import AsyncClient
from app.config.setting import Settings

settings = Settings()

def create_event_provider_client() -> AsyncClient:
    return AsyncClient(
        base_url=settings.EVENT_PROVIDER_URL,
        headers={
            "x-api-key": settings.EVENT_PROVIDER_API_KEY,
        },
        follow_redirects=True
    )
