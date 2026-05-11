from pathlib import Path

import yaml
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.logging_config import setup_logging
from app.metrics import metrics, prometheus_middleware
from app.routers import bookings, fines, registration

setup_logging()

app = FastAPI(
    title="Car Rent API",
    description="API для регистрации, бронирования автомобилей и штрафов",
    version="1.0.0",
    docs_url="/docs",
)

app.middleware("http")(prometheus_middleware)

app.include_router(registration.router)
app.include_router(bookings.router)
app.include_router(fines.router)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/swagger", include_in_schema=False)
async def swagger() -> RedirectResponse:
    return RedirectResponse(url="/docs")


app.add_api_route("/metrics", metrics, methods=["GET"], include_in_schema=False)


def custom_openapi() -> dict:
    spec_path = Path(__file__).resolve().parents[1] / "spec" / "openapi.yaml"
    with spec_path.open(encoding="utf-8") as spec_file:
        return yaml.safe_load(spec_file)


app.openapi = custom_openapi
