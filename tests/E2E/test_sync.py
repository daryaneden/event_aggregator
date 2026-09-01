import pytest


@pytest.mark.asyncio
async def test_trigger_sync_returns_success(
    client,
    sync_events_use_case,
):
    response = await client.post("/api/sync/trigger")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Synchronization started",
    }

    sync_events_use_case.execute.assert_awaited_once_with()