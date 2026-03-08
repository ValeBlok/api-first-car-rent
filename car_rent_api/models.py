from pydantic import BaseModel
from datetime import datetime

class Car(BaseModel):
    brand: str
    model: str
    price_per_hour: float

class UserCreation(BaseModel):
    license_number: int
    name: str
    surname: str
    age: int
    fine_count: int = 0

class BookingRequest(BaseModel):
    car_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
