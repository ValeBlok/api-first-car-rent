from time import perf_counter

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.middleware.base import RequestResponseEndpoint

from app import storage


REQUEST_COUNT = Counter(
    "car_rent_http_requests_total",
    "Total number of HTTP requests.",
    ["method", "path", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "car_rent_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)
REQUESTS_IN_PROGRESS = Gauge(
    "car_rent_http_requests_in_progress",
    "Number of HTTP requests currently being processed.",
    ["method"],
)
USERS_TOTAL = Gauge(
    "car_rent_users_total",
    "Current number of registered users.",
)
BOOKINGS_TOTAL = Gauge(
    "car_rent_bookings_total",
    "Current number of active bookings.",
)
FINES_TOTAL = Gauge(
    "car_rent_fines_total",
    "Current number of created fines.",
)


def get_route_path(request: Request) -> str:
    route = request.scope.get("route")
    return getattr(route, "path", request.url.path)


async def prometheus_middleware(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    if request.url.path == "/metrics":
        return await call_next(request)

    method = request.method
    start_time = perf_counter()
    status_code = 500

    REQUESTS_IN_PROGRESS.labels(method=method).inc()
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        route_path = get_route_path(request)
        duration = perf_counter() - start_time

        REQUEST_COUNT.labels(
            method=method,
            path=route_path,
            status_code=str(status_code),
        ).inc()
        REQUEST_LATENCY.labels(method=method, path=route_path).observe(duration)
        REQUESTS_IN_PROGRESS.labels(method=method).dec()


async def metrics() -> Response:
    USERS_TOTAL.set(len(storage.users))
    BOOKINGS_TOTAL.set(len(storage.bookings))
    FINES_TOTAL.set(sum(len(user_fines) for user_fines in storage.fines.values()))

    return Response(generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})
