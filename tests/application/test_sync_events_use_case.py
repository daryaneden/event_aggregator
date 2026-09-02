from datetime import datetime
from unittest.mock import Mock

import pytest

from app.application.use_cases.sync_events import SyncEventsUseCase
from app.domain.entities.sync_state import SyncState, SyncStatus


@pytest.mark.asyncio
async def test_execute_syncs_events_successfully(provider,
                                                 uow_factory,
                                                 event_repository,
                                                 sync_state_repository,
                                                 patch_events_paginator):
    
    sync_state_repository.get.return_value = None

    event_1 = Mock()
    event_1.changed_at = datetime(2026, 8, 20, 10, 0)

    event_2 = Mock()
    event_2.changed_at = datetime(2026, 8, 21, 10, 0)

    class FakePaginator:
        def __init__(self, provider, changed_at):
            self.changed_at = changed_at

        def __aiter__(self):
            async def iterate():
                yield event_1
                yield event_2

            return iterate()

    patch_events_paginator(FakePaginator)

    use_case = SyncEventsUseCase(provider=provider,
                                 uow_factory=uow_factory)

    await use_case.execute()

    event_repository.save.assert_any_await(event_1)
    event_repository.save.assert_any_await(event_2)
    assert event_repository.save.await_count == 2

    saved_state = sync_state_repository.save.await_args_list[-1].args[0]

    assert saved_state.sync_status == SyncStatus.SUCCESS
    assert saved_state.last_changed_at == event_2.changed_at
    assert saved_state.last_sync_time is not None


@pytest.mark.asyncio
async def test_execute_uses_existing_last_changed_at(provider,
                                                     uow_factory,
                                                     sync_state_repository,
                                                     patch_events_paginator):
    
    previous_changed_at = datetime(2026, 8, 20, 10, 0)

    sync_state_repository.get.return_value = SyncState(last_sync_time=datetime(2026, 8, 20, 11, 0),
                                                       last_changed_at=previous_changed_at,
                                                       sync_status=SyncStatus.SUCCESS)

    paginator_args = {}

    class FakePaginator:
        def __init__(self, provider, changed_at):
            paginator_args['changed_at'] = changed_at

        def __aiter__(self):
            async def iterate():
                return
                yield

            return iterate()

    patch_events_paginator(FakePaginator)

    use_case = SyncEventsUseCase(provider=provider,
                                 uow_factory=uow_factory)

    await use_case.execute()

    assert paginator_args['changed_at'] == previous_changed_at

@pytest.mark.asyncio
async def test_execute_sets_failed_status_when_sync_fails(provider,
                                                          uow_factory,
                                                          sync_state_repository,
                                                          patch_events_paginator):
    sync_state_repository.get.return_value = None

    class FakePaginator:
        def __init__(self, provider, changed_at):
            pass

        def __aiter__(self):
            async def iterate():
                raise RuntimeError('provider error')
                yield

            return iterate()

    patch_events_paginator(FakePaginator)

    use_case = SyncEventsUseCase(provider=provider,
                                 uow_factory=uow_factory)

    with pytest.raises(RuntimeError, match='provider error'):
        await use_case.execute()

    saved_states = [call.args[0] for call in sync_state_repository.save.await_args_list]

    statuses = [state.sync_status for state in saved_states]

    assert SyncStatus.RUNNING in statuses
    assert SyncStatus.FAILED in statuses

