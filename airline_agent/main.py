from fastapi import FastAPI, HTTPException

from airline_agent.models.flight import (
    Flight,
    FlightSearchRequest,
    FlightSearchResponse,
)

from airline_agent.models.booking import (
    BookingRequest,
    BookingResponse,
)


app = FastAPI(
    title="QForge Airline API",
    version="0.1.0",
)


# Mock flight data
FLIGHTS = [
    Flight(
        flight_id="F101",
        origin="DFW",
        destination="ORD",
        departure_time="15:00",
        arrival_time="18:30",
        additional_cost=120,
        available_seats=5,
    ),
    Flight(
        flight_id="F102",
        origin="DFW",
        destination="ORD",
        departure_time="17:30",
        arrival_time="21:00",
        additional_cost=80,
        available_seats=7,
    ),
    Flight(
        flight_id="F103",
        origin="DFW",
        destination="ORD",
        departure_time="16:00",
        arrival_time="19:15",
        additional_cost=250,
        available_seats=3,
    ),
]


# Temporary in-memory booking store
BOOKINGS = []


@app.post("/flights/search", response_model=FlightSearchResponse)
def search_flights(request: FlightSearchRequest):

    matching_flights = [
        flight
        for flight in FLIGHTS
        if flight.origin == request.origin
        and flight.destination == request.destination
    ]

    return FlightSearchResponse(
        flights=matching_flights
    )


@app.post("/bookings", response_model=BookingResponse)
def create_booking(request: BookingRequest):

    flight = next(
        (
            flight
            for flight in FLIGHTS
            if flight.flight_id == request.flight_id
        ),
        None,
    )

    if flight is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "FLIGHT_NOT_FOUND",
                "message": f"Flight {request.flight_id} does not exist.",
            },
        )

    if flight.available_seats <= 0:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "NO_SEATS_AVAILABLE",
                "message": f"No seats are available for flight {request.flight_id}.",
            },
        )

    booking = BookingResponse(
        booking_id=f"B{9000 + len(BOOKINGS) + 1}",
        passenger_id=request.passenger_id,
        flight_id=request.flight_id,
        status="CONFIRMED",
    )

    BOOKINGS.append(booking)

    return booking