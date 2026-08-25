from app.application.interfaces.event_provider import EventsProvider
from app.application.interfaces.uow import UnitOfWork
from app.domain.entities.sync_state import SyncState

from datetime import datetime

INITIAL_CHANGED_AT = datetime(2000, 1, 1)

class SyncEventsUseCase:

    def __init__(self, events_provider: EventsProvider, uow: UnitOfWork):

        self.events_provider = events_provider
        self.uow = uow

    async def execute(self, changed_at) -> None:

        self.events_provider.get_events(changed_at)

        sync_state = await self.uow.sync_state_repository.get()

        changed_at = (sync_state.last_changed_at if sync_state else INITIAL_CHANGED_AT)

        events = await self.events_provider.get_events(changed_at)

        if not events:
            return

        last_changed_at = max(event.changed_at for event in events)

        async with self.uow:

            await self.uow.event_repository.save(events)

            new_sync_state = SyncState(id=1, 
                                        last_sync_time=datetime.now(),
                                        last_changed_at=last_changed_at,
                                        sync_status="SUCCESS")

            await self.uow.sync_state_repository.save(new_sync_state)