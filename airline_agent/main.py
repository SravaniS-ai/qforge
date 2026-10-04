from fastapi import FastAPI

from airline_agent.models.booking import (
    BookingRequest,
    BookingResponse,
)

from airline_agent.models.flight import (
    FlightSearchRequest,
    FlightSearchResponse,
)

from airline_agent.services.airline_service import (
    create_booking,
    search_flights,
)

from airline_agent.agents.rebooking_agent import rebook_passenger
from airline_agent.models.rebooking import (
    RebookingRequest,
    RebookingResult,
)

app = FastAPI(
    title="QForge Airline API",
    version="0.1.0",
)


@app.post(
    "/flights/search",
    response_model=FlightSearchResponse,
)
def search_flights_endpoint(
    request: FlightSearchRequest,
):
    flights = search_flights(
        origin=request.origin,
        destination=request.destination,
    )

    return FlightSearchResponse(
        flights=flights
    )


@app.post(
    "/bookings",
    response_model=BookingResponse,
)
def create_booking_endpoint(
    request: BookingRequest,
):
    return create_booking(request)

@app.post(
    "/rebook",
    response_model=RebookingResult,
)
def rebook_endpoint(
    request: RebookingRequest,
):
    return rebook_passenger(request)