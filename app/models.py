from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class UserCreate(BaseModel):
    license_number: int = Field(gt=0)
    name: str = Field(min_length=1)
    surname: str = Field(min_length=1)
    age: int = Field(ge=18)
    fine_count: int = Field(default=0, ge=0)


class UserCreated(BaseModel):
    user_id: int
    message: str


class BookingCreate(BaseModel):
    car_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time_range(self) -> "BookingCreate":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


class BookingCreated(BaseModel):
    booking_id: int
    car_id: int
    user_id: int
    total_price: float
    status: Literal["confirmed"]


class BookingCancelled(BaseModel):
    booking_id: int
    status: Literal["cancelled"]
    message: str


class FineCreate(BaseModel):
    user_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    reason: str = Field(min_length=1)


class FineCreated(BaseModel):
    fine_id: int
    user_id: int
    amount: float
    reason: str
    status: Literal["created"]


class UserFines(BaseModel):
    user_id: int
    has_fines: bool
    fines_count: int
    total_amount: float
    message: str
