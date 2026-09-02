from datetime import UTC, datetime

import pytest

from app.domain.entities.sync_state import SyncState, SyncStatus


@pytest.mark.asyncio
async def test_save_and_get_sync_state(
    sync_state_repository,
    test_session,
):
    sync_state = SyncState(last_sync_time=datetime(2026, 8, 28, 12, 0, tzinfo=UTC),
                           last_changed_at=datetime(2026, 8, 28, 11, 30, tzinfo=UTC),
                           sync_status=SyncStatus.SUCCESS)

    await sync_state_repository.save(sync_state)
    await test_session.commit()

    result = await sync_state_repository.get()

    assert result is not None
    assert result.last_sync_time == sync_state.last_sync_time
    assert result.last_changed_at == sync_state.last_changed_at
    assert result.sync_status == SyncStatus.SUCCESS


@pytest.mark.asyncio
async def test_get_returns_none_when_sync_state_does_not_exist(
    sync_state_repository,
):
    result = await sync_state_repository.get()

    assert result is None
