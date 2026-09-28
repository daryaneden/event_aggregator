from abc import ABC, abstractmethod


class NotificationClient(ABC):

    @abstractmethod
    async def send_notification(self,
                                message: str,
                                reference_id: str,
                                idempotency_key: str) -> None:
        pass