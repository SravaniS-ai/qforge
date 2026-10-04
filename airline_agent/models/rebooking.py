from datetime import date, time

from pydantic import BaseModel, Field

from airline_agent.models.booking import BookingResponse
from airline_agent.models.flight import Flight


class RebookingRequest(BaseModel):
    passenger_id: str
    origin: str
    destination: str
    travel_date: date
    arrival_deadline: time
    max_additional_cost: float = Field(ge=0)


class RebookingResult(BaseModel):
    status: str
    message: str
    selected_flight: Flight | None = None
    booking: BookingResponse | None = None  