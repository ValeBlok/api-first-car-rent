from fastapi import APIRouter, HTTPException
from models import BookingRequest
import random

router = APIRouter(tags=["Bookings"])

@router.post("/bookings")
async def create_booking(booking: BookingRequest):
    hours = (booking.end_time - booking.start_time).total_seconds() / 3600
    total_price = 200 * hours
    
    return {
        "booking_id": random.randint(1, 100),
        "car_id": booking.car_id,
        "user_id": booking.user_id,
        "total_price": total_price,
        "status": "confirmed"
    }

@router.delete("/bookings/{booking_id}")
async def cancel_booking(booking_id: int):
    booking_exists = True
    can_cancel = True
    
    if not booking_exists:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    
    if not can_cancel:
        raise HTTPException(status_code=400, detail="Бронь нельзя отменить")
    
    return {
        "booking_id": booking_id,
        "status": "cancelled",
        "message": "Бронирование успешно отменено"
    }