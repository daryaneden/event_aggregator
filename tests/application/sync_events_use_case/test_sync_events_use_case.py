from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from app.application.use_cases.sync_events import (
    SyncEventsUseCase,
)
from app.domain.entities.event import Event
from app.domain.entities.place import Place
from app.domain.entities.sync_state import SyncState
from app.domain.entities.sync_state import SyncStatus
from app.application.models.events_page import EventsPage


def create_event(
    name: str,
    changed_at: datetime,
) -> Event:
    return Event(
        id=uuid4(),
        name=name,
        place=Place(
            id=uuid4(),
            name="Arena",
            city="Helsinki",
            address="Main street 1",
            seats_pattern="pattern",
        ),
        event_time=datetime(2026, 9, 1, 18, 0),
        registration_deadline=datetime(2026, 8, 30, 18, 0),
        status="active",
        number_of_visitors=100,
        changed_at=changed_at,
        created_at=datetime(2026, 8, 1, 10, 0),
        status_changed_at=changed_at,
    )


def create_uow(
    sync_state: SyncState | None = None,
):
    sync_state_repository = AsyncMock()
    sync_state_repository.get.return_value = sync_state

    event_repository = AsyncMock()

    uow = AsyncMock()
    uow.sync_state_repository = sync_state_repository
    uow.event_repository = event_repository

    uow.__aenter__.return_value = uow

    return uow

@pytest.mark.asyncio
async def test_first_sync_uses_initial_date_and_saves_events():
    event_1 = create_event(
        "Concert",
        datetime(2026, 8, 21, 10, 0),
    )

    event_2 = create_event(
        "Theatre",
        datetime(2026, 8, 21, 12, 0),
    )

    provider = Mock()

    provider.get_events_page = AsyncMock(
        return_value=EventsPage(
            events=[event_1, event_2],
            next_url=None,
        ),
    )

    running_uow = create_uow()
    sync_uow = create_uow()

    uow_factory = Mock(
        side_effect=[
            running_uow,
            sync_uow,
        ],
    )

    use_case = SyncEventsUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    await use_case.execute()

    provider.get_events_page.assert_awaited_once_with(
        changed_at=datetime(2000, 1, 1),
        url=None,
    )

    assert (
        sync_uow.event_repository.save.await_count
        == 2
    )

    sync_uow.event_repository.save.assert_any_await(
        event_1
    )

    sync_uow.event_repository.save.assert_any_await(
        event_2
    )

@pytest.mark.asyncio
async def test_subsequent_sync_uses_last_changed_at_and_updates_cursor():
    previous_changed_at = datetime(
        2026,
        8,
        20,
        10,
        0,
    )

    event_1 = create_event(
        "Concert",
        datetime(2026, 8, 21, 10, 0),
    )

    event_2 = create_event(
        "Theatre",
        datetime(2026, 8, 21, 12, 0),
    )

    provider = Mock()

    provider.get_events_page = AsyncMock(
        return_value=EventsPage(
            events=[event_1, event_2],
            next_url=None,
        ),
    )

    sync_state = SyncState(
        last_sync_time=datetime(
            2026,
            8,
            20,
            12,
            0,
        ),
        last_changed_at=previous_changed_at,
        sync_status=SyncStatus.SUCCESS,
    )

    running_uow = create_uow()
    sync_uow = create_uow(sync_state)

    uow_factory = Mock(
        side_effect=[
            running_uow,
            sync_uow,
        ],
    )

    use_case = SyncEventsUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    await use_case.execute()

    provider.get_events_page.assert_awaited_once_with(
        changed_at=previous_changed_at,
        url=None,
    )

    saved_state = (
        sync_uow.sync_state_repository.save.call_args.args[0]
    )

    assert (
        saved_state.last_changed_at
        == datetime(2026, 8, 21, 12, 0)
    )

@pytest.mark.asyncio
async def test_successful_sync_sets_success_status():
    event = create_event(
        "Concert",
        datetime(2026, 8, 21, 10, 0),
    )

    provider = Mock()

    provider.get_events_page = AsyncMock(
        return_value=EventsPage(
            events=[event],
            next_url=None,
        ),
    )

    running_uow = create_uow()

    sync_state = SyncState(
        last_sync_time=None,
        last_changed_at=datetime(
            2026,
            8,
            20,
            10,
            0,
        ),
        sync_status=SyncStatus.RUNNING,
    )

    sync_uow = create_uow(sync_state)

    uow_factory = Mock(
        side_effect=[
            running_uow,
            sync_uow,
        ],
    )

    use_case = SyncEventsUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    await use_case.execute()

    saved_state = (
        sync_uow.sync_state_repository.save.call_args.args[0]
    )

    assert saved_state.sync_status == SyncStatus.SUCCESS
    assert saved_state.last_sync_time is not None

@pytest.mark.asyncio
async def test_failed_sync_sets_failed_status_and_reraises():
    provider = Mock()

    provider.get_events_page = AsyncMock(
        side_effect=RuntimeError("Provider error"),
    )

    running_uow = create_uow()

    sync_state = SyncState(
        last_sync_time=None,
        last_changed_at=datetime(
            2026,
            8,
            20,
            10,
            0,
        ),
        sync_status=SyncStatus.RUNNING,
    )

    sync_uow = create_uow(sync_state)
    failed_uow = create_uow(sync_state)

    uow_factory = Mock(
        side_effect=[
            running_uow,
            sync_uow,
            failed_uow,
        ],
    )

    use_case = SyncEventsUseCase(
        provider=provider,
        uow_factory=uow_factory,
    )

    with pytest.raises(
        RuntimeError,
        match="Provider error",
    ):
        await use_case.execute()

    saved_state = (
        failed_uow.sync_state_repository.save.call_args.args[0]
    )

    assert saved_state.sync_status == SyncStatus.FAILED