import time

from fastapi import Request

from app.infrastructure.metrics import (
    http_request_duration_seconds,
    http_requests_total,
)


def get_endpoint(request: Request) -> str:
    route = request.scope.get("route")

    if route is not None:
        return route.path

    return request.url.path


async def metrics_middleware(request: Request, call_next):
    start_time = time.monotonic()

    try:
        response = await call_next(request)
    except Exception:
        duration = time.monotonic() - start_time
        endpoint = get_endpoint(request)

        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status="500",
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

        raise

    duration = time.monotonic() - start_time
    endpoint = get_endpoint(request)

    http_requests_total.labels(
        method=request.method,
        endpoint=endpoint,
        status=str(response.status_code),
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=endpoint,
    ).observe(duration)

    return response