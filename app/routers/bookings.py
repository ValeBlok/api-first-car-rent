from fastapi import APIRouter, HTTPException, status

from app import storage
from app.models import BookingCancelled, BookingCreate, BookingCreated

router = APIRouter(tags=["Bookings"])


@router.post(
    "/bookings",
    operation_id="createBooking",
    response_model=BookingCreated,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(booking: BookingCreate) -> BookingCreated:
    booking_id = storage.next_booking_id
    storage.next_booking_id += 1

    hours = (booking.end_time - booking.start_time).total_seconds() / 3600
    total_price = storage.PRICE_PER_HOUR * hours

    created_booking = BookingCreated(
        booking_id=booking_id,
        car_id=booking.car_id,
        user_id=booking.user_id,
        total_price=total_price,
        status="confirmed",
    )
    storage.bookings[booking_id] = created_booking.model_dump()

    return created_booking


@router.delete(
    "/bookings/{booking_id}",
    operation_id="cancelBooking",
    response_model=BookingCancelled,
)
async def cancel_booking(booking_id: int) -> BookingCancelled:
    if booking_id not in storage.bookings:
        raise HTTPException(status_code=404, detail="Бронь не найдена")

    storage.bookings.pop(booking_id)

    return BookingCancelled(
        booking_id=booking_id,
        status="cancelled",
        message="Бронирование успешно отменено",
    )
