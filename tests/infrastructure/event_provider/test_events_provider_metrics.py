import httpx
import pytest

@pytest.mark.asyncio
async def test_request_records_success_metrics(
    events_provider,
    http_client,
    events_provider_metrics_test_setup,
):
    requests_counter, duration_histogram = (
        events_provider_metrics_test_setup
    )

    response = httpx.Response(
        status_code=200,
        request=httpx.Request(
            "GET",
            "https://example.com/api/events/",
        ),
    )
    http_client.request.return_value = response

    result = await events_provider._request(
        method="GET",
        url="/api/events/",
        endpoint="/events",
    )

    assert result.status_code == 200
    requests_counter.labels.assert_called_once_with(
        endpoint="/events",
        status="200",
    )
    requests_counter.labels.return_value.inc.assert_called_once()
    duration_histogram.labels.return_value.observe.assert_called_once()

@pytest.mark.asyncio
async def test_request_records_failure_metrics(
    events_provider,
    http_client,
    events_provider_metrics_test_setup,
):
    requests_counter, duration_histogram = (
        events_provider_metrics_test_setup
    )

    http_client.request.side_effect = httpx.ConnectError(
        "Connection failed",
        request=httpx.Request(
            "GET",
            "https://example.com/api/events/",
        ),
    )

    with pytest.raises(httpx.ConnectError):
        await events_provider._request(
            method="GET",
            url="/api/events/",
            endpoint="/events",
        )

    requests_counter.labels.assert_called_once_with(
        endpoint="/events",
        status="error",
    )
    requests_counter.labels.return_value.inc.assert_called_once()
    duration_histogram.labels.return_value.observe.assert_called_once()