from datetime import date, time

from pydantic import BaseModel, Field


class FlightSearchRequest(BaseModel):
    origin: str
    destination: str
    travel_date: date


class Flight(BaseModel):
    flight_id: str
    origin: str
    destination: str
    departure_time: time
    arrival_time: time
    additional_cost: float = Field(ge=0)
    available_seats: int = Field(ge=0)


class FlightSearchResponse(BaseModel):
    flights: list[Flight]