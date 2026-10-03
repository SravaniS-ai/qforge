import pytest
from pydantic import ValidationError

from airline_agent.models.flight import Flight


def test_valid_flight():
    flight = Flight(
        flight_id="F101",
        origin="DFW",
        destination="ORD",
        departure_time="15:00",
        arrival_time="18:30",
        additional_cost=120,
        available_seats=5,
    )

    assert flight.flight_id == "F101"
    assert flight.additional_cost == 120
    assert flight.available_seats == 5


def test_negative_additional_cost_is_rejected():
    with pytest.raises(ValidationError):
        Flight(
            flight_id="F101",
            origin="DFW",
            destination="ORD",
            departure_time="15:00",
            arrival_time="18:30",
            additional_cost=-100,
            available_seats=5,
        )