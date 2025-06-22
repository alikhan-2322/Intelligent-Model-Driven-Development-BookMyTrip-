# booking_tools.py

from trips_data import TRIPS

# build a lookup by trip id
_TRIP_INDEX = {t["id"]: t for t in TRIPS}

# in-memory bookings store
_BOOKINGS = {}

def search_trips(trips, max_budget):
    """
    Return all trips whose price <= max_budget.
    """
    return [t for t in trips if t["price"] <= max_budget]

def book_trip(user_id: str, trip_id: str) -> dict:
    """
    Create a new booking for user_id on trip_id.
    Returns the booking record.
    """
    if trip_id not in _TRIP_INDEX:
        raise ValueError(f"No such trip: {trip_id}")
    booking_id = f"B{len(_BOOKINGS)+1}"
    record = {
        "booking_id": booking_id,
        "user_id": user_id,
        "trip_id": trip_id,
        "status": "confirmed"
    }
    _BOOKINGS[booking_id] = record
    return record

def cancel_booking(booking_id: str) -> bool:
    """
    Cancel an existing booking. Returns True if successful.
    """
    rec = _BOOKINGS.get(booking_id)
    if not rec:
        return False
    rec["status"] = "canceled"
    return True
