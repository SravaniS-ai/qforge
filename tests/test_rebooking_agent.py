from airline_agent.agents.rebooking_agent import rebook_passenger
from airline_agent.models.rebooking import RebookingRequest


def test_rebooking_agent_selects_eligible_flight():

    request = RebookingRequest(
        passenger_id="P123",
        origin="DFW",
        destination="ORD",
        travel_date="2026-10-04",
        arrival_deadline="20:00",
        max_additional_cost=200,
    )

    result = rebook_passenger(request)

    assert result.status == "CONFIRMED"
    assert result.selected_flight is not None
    assert result.selected_flight.flight_id == "F101"

    assert result.booking is not None
    assert result.booking.flight_id == "F101"
    assert result.booking.status == "CONFIRMED"


def test_rebooking_agent_returns_no_eligible_flight():

    request = RebookingRequest(
        passenger_id="P123",
        origin="DFW",
        destination="ORD",
        travel_date="2026-10-04",
        arrival_deadline="17:00",
        max_additional_cost=100,
    )

    result = rebook_passenger(request)

    assert result.status == "NO_ELIGIBLE_FLIGHT"
    assert result.selected_flight is None
    assert result.booking is None   