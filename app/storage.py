users: dict[int, dict] = {}
bookings: dict[int, dict] = {}
fines: dict[int, list[dict]] = {}

next_user_id = 1
next_booking_id = 1
next_fine_id = 1

PRICE_PER_HOUR = 200
