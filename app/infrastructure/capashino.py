from httpx import AsyncClient

from app.application.interfaces.notification_client import NotificationClient


class CapashinoClient(NotificationClient):

    def __init__(
        self,
        client: AsyncClient,
    ):
        self.client = client

    async def send_notification(
        self,
        message: str,
        reference_id: str,
        idempotency_key: str,
    ) -> None:

        payload = {
            "message": message,
            "reference_id": reference_id,
            "idempotency_key": idempotency_key,
        }

        print("CAPASHINO PAYLOAD:", payload)
        
        response = await self.client.post(
            "/api/notifications",
            json={
                "message": message,
                "reference_id": reference_id,
                "idempotency_key": idempotency_key,
            },
        )

        print("CAPASHINO STATUS:", response.status_code)
        print("CAPASHINO RESPONSE:", response.text)


        response.raise_for_status()