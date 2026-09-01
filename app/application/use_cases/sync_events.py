import logging
from collections.abc import Callable
from datetime import UTC, datetime

from app.application.interfaces.events_provider import EventsProvider
from app.application.interfaces.uow import UnitOfWork
from app.domain.entities.sync_state import SyncState, SyncStatus
from app.infrastructure.event_provider.events_paginator import EventsPaginator

logger = logging.getLogger(__name__)

FIRST_SYNC_DATE = datetime(2000, 1, 1, tzinfo=UTC)

class SyncEventsUseCase:

    def __init__(self, provider: EventsProvider,
                 uow_factory: Callable[[], UnitOfWork]):
        
        self.provider = provider
        self.uow_factory = uow_factory

    async def execute(self) -> None:

        logger.info('Events synchronization started')

        await self._set_status(SyncStatus.RUNNING)

        try:
            await self._sync()

        except Exception:
            logger.exception('Events synchronization failed')

            await self._set_status(SyncStatus.FAILED)

            raise

        logger.info('Events synchronization completed successfully')

    async def _sync(self) -> None:

        async with self.uow_factory() as uow:

            sync_state = await uow.sync_state_repository.get()

            changed_at = (sync_state.last_changed_at
                          if sync_state 
                          and sync_state.last_changed_at
                          else FIRST_SYNC_DATE)

            last_changed_at = (sync_state.last_changed_at
                               if sync_state
                               else None)

            logger.info('Starting events sync from changed_at=%s', changed_at)

            paginator = EventsPaginator(provider=self.provider,
                                        changed_at=changed_at)

            events_count = 0

            async for event in paginator:

                await uow.event_repository.save(event)

                events_count +=1

                if (last_changed_at is None
                    or event.changed_at > last_changed_at):
                    last_changed_at = event.changed_at

            await uow.sync_state_repository.save(SyncState(
                last_sync_time=datetime.now(UTC),
                last_changed_at=last_changed_at,
                sync_status=SyncStatus.SUCCESS))

            logger.info('Events synchronization finished: '
                            'events_processed=%s, last_changed_at=%s',
                            events_count,
                            last_changed_at)

    async def _set_status(self, status: SyncStatus) -> None:

        async with self.uow_factory() as uow:

            sync_state = await uow.sync_state_repository.get()

            if sync_state is None:
                sync_state = SyncState(last_sync_time=None,
                                       last_changed_at=None,
                                       sync_status=status)
            else:
                sync_state.sync_status = status

            await uow.sync_state_repository.save(sync_state)
