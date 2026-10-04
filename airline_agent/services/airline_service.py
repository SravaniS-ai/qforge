from fastapi import HTTPException

from airline_agent.models.booking import (
    BookingRequest,
    BookingResponse,
)

from airline_agent.models.flight import Flight


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


BOOKINGS = []


def search_flights(origin: str, destination: str) -> list[Flight]:
    return [
        flight
        for flight in FLIGHTS
        if flight.origin == origin
        and flight.destination == destination
    ]


def create_booking(request: BookingRequest) -> BookingResponse:

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