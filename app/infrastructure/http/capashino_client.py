from httpx import AsyncClient

from app.config.setting import Settings

settings = Settings()

def create_capashino_client() -> AsyncClient:
    return AsyncClient(base_url=settings.CAPASHINO_CLIENT_URL,
                       headers={'x-api-key': settings.EVENT_PROVIDER_API_KEY},
                       follow_redirects=True)