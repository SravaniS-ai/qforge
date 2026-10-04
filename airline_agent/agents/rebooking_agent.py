from airline_agent.models.booking import BookingRequest
from airline_agent.models.rebooking import (
    RebookingRequest,
    RebookingResult,
)
from airline_agent.services.airline_service import (
    create_booking,
    search_flights,
)


def rebook_passenger(
    request: RebookingRequest,
) -> RebookingResult:

    # Step 1: Search available flights
    flights = search_flights(
        origin=request.origin,
        destination=request.destination,
    )

    # Step 2: Apply passenger constraints
    eligible_flights = [
        flight
        for flight in flights
        if flight.arrival_time <= request.arrival_deadline
        and flight.additional_cost <= request.max_additional_cost
        and flight.available_seats > 0
    ]

    # Step 3: Handle case where nothing qualifies
    if not eligible_flights:
        return RebookingResult(
            status="NO_ELIGIBLE_FLIGHT",
            message="No flight satisfies the passenger constraints.",
        )

    # Step 4: Select the cheapest eligible flight.
    # If costs are equal, prefer the earlier arrival.
    selected_flight = min(
        eligible_flights,
        key=lambda flight: (
            flight.additional_cost,
            flight.arrival_time,
        ),
    )

    # Step 5: Create the booking
    booking = create_booking(
        BookingRequest(
            passenger_id=request.passenger_id,
            flight_id=selected_flight.flight_id,
        )
    )

    # Step 6: Return the result
    return RebookingResult(
        status="CONFIRMED",
        message="Passenger successfully rebooked.",
        selected_flight=selected_flight,
        booking=booking,
    )