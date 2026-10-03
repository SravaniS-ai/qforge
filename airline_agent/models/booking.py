from pydantic import BaseModel


class BookingRequest(BaseModel):
    passenger_id: str
    flight_id: str


class BookingResponse(BaseModel):
    booking_id: str
    passenger_id: str
    flight_id: str
    status: str