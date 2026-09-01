from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.sync_state_repository import SyncStateRepository
from app.domain.entities.sync_state import SyncState
from app.infrastructure.database.models.sync_state import SyncStateModel


class SqlAlchemySyncStateRepository(SyncStateRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self) -> SyncState | None:

        query = select(SyncStateModel).where(SyncStateModel.id == 1)

        sync_state_model = (await self.session.execute(query)).scalar_one_or_none()

        if sync_state_model is None:
            return None

        return await self._to_domain(sync_state_model)

    async def save(self, sync_state: SyncState) -> None:

        model = await self.session.get(SyncStateModel, 1)

        if model is None:

            model = SyncStateModel(last_sync_time=sync_state.last_sync_time,
                                   last_changed_at=sync_state.last_changed_at,
                                   sync_status=sync_state.sync_status)

            self.session.add(model)

        else:

            model.last_sync_time = sync_state.last_sync_time
            model.last_changed_at = sync_state.last_changed_at
            model.sync_status = sync_state.sync_status

    async def _to_domain (self, model: SyncStateModel) -> SyncState:

        return SyncState(last_sync_time=model.last_sync_time,
                         last_changed_at=model.last_changed_at,
                         sync_status=model.sync_status)