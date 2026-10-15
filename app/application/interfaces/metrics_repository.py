from abc import ABC, abstractmethod


class MetricsRepository(ABC):
    @abstractmethod
    async def get_tickets_count(self) -> int:
        pass

    @abstractmethod
    async def get_cancelled_tickets_count(self) -> int:
        pass

    @abstractmethod
    async def get_events_count(self) -> int:
        pass