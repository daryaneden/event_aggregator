from abc import ABC, abstractmethod

from app.domain.entities.sync_state import SyncState


class SyncStateRepository(ABC):

    @abstractmethod
    async def get(self) -> SyncState | None:
        pass

    @abstractmethod
    async def save(self, sync_state: SyncState) -> None:
        pass