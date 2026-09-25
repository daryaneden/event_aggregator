from abc import ABC, abstractmethod

from app.application.dtos.outbox_message import OutboxMessageDto


class OutboxRepository(ABC):

    @abstractmethod
    async def save(self, message: OutboxMessageDto) -> None:
        pass