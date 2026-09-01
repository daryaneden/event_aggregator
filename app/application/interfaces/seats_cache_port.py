from abc import ABC, abstractmethod
from uuid import UUID


class SeatsCachePort(ABC):

    @abstractmethod
    def get(self, event_id: UUID) -> list[str] | None:
        pass

    @abstractmethod
    def set(self, event_id: UUID, seats: list[str]) -> None:
        pass