from fastapi import FastAPI
from routers import registration, bookings, fines
from fastapi import FastAPI

app = FastAPI(
    title="CarRent API",
    description="API для аренды автомобилей",
    version="1.0.0",
    docs_url="/docs"
)

app.include_router(registration.router)
app.include_router(bookings.router)
app.include_router(fines.router)
