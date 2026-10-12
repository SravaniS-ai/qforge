from airline_agent.models.booking import BookingResponse
from airline_agent.models.flight import Flight
from airline_agent.models.rebooking import RebookingResult

from qforge.evaluators.checks import (
    build_booking_created_check,
    evaluate_arrival_deadline,
    evaluate_booking_match,
    evaluate_cost_constraint,
    evaluate_destination,
    evaluate_no_booking_created,
    evaluate_no_flight_selected,
    evaluate_status,
)
from qforge.scenarios.qf_001 import QF_001
from qforge.scenarios.qf_002 import QF_002


def build_valid_qf_001_result() -> RebookingResult:
    """
    Create a valid observed result for QF-001.

    Multiple evaluator-check tests reuse this object so that each
    test can focus on one evaluation rule instead of rebuilding
    the same result repeatedly.
    """

    selected_flight = Flight(
        flight_id="F101",
        origin="DFW",
        destination="ORD",
        departure_time="15:00",
        arrival_time="18:30",
        additional_cost=120,
        available_seats=5,
    )

    booking = BookingResponse(
        booking_id="B9001",
        passenger_id="P123",
        flight_id="F101",
        status="CONFIRMED",
    )

    return RebookingResult(
        status="CONFIRMED",
        message="Passenger successfully rebooked.",
        selected_flight=selected_flight,
        booking=booking,
    )


def test_status_check_passes_for_expected_status():
    """
    QF-001 expects CONFIRMED, so a CONFIRMED agent result
    should pass the status evaluator.
    """

    result = build_valid_qf_001_result()

    check = evaluate_status(
        scenario=QF_001,
        result=result,
    )

    assert check.name == "status"
    assert check.status == "PASS"


def test_arrival_deadline_check_detects_late_flight():
    """
    Verify the arrival rule independently from the full evaluator.
    """

    result = build_valid_qf_001_result()

    # Deliberately replace the selected flight with one that arrives
    # after QF-001's 20:00 arrival deadline.
    result.selected_flight = Flight(
        flight_id="F102",
        origin="DFW",
        destination="ORD",
        departure_time="17:30",
        arrival_time="21:00",
        additional_cost=80,
        available_seats=7,
    )

    check = evaluate_arrival_deadline(
        scenario=QF_001,
        result=result,
    )

    assert check.name == "arrival_deadline"
    assert check.status == "FAIL"


def test_cost_check_detects_over_budget_flight():
    """
    Verify the cost rule independently from the full evaluator.
    """

    result = build_valid_qf_001_result()

    # F103 satisfies the arrival deadline but exceeds QF-001's
    # maximum additional cost of $200.
    result.selected_flight = Flight(
        flight_id="F103",
        origin="DFW",
        destination="ORD",
        departure_time="16:00",
        arrival_time="19:15",
        additional_cost=250,
        available_seats=3,
    )

    check = evaluate_cost_constraint(
        scenario=QF_001,
        result=result,
    )

    assert check.name == "cost_constraint"
    assert check.status == "FAIL"


def test_booking_match_check_detects_mismatch():
    """
    Verify that the selected flight and booked flight must agree.
    """

    result = build_valid_qf_001_result()

    # The agent claims F101 was selected, but the booking points
    # to F103. This should fail consistency validation.
    result.booking = BookingResponse(
        booking_id="B9002",
        passenger_id="P123",
        flight_id="F103",
        status="CONFIRMED",
    )

    check = evaluate_booking_match(
        result=result,
    )

    assert check.name == "booking_matches_selected_flight"
    assert check.status == "FAIL"


def test_no_flight_selected_check_passes_for_qf_002():
    """
    QF-002 expects NO_ELIGIBLE_FLIGHT, so having no selected
    flight is correct behavior.
    """

    result = RebookingResult(
        status="NO_ELIGIBLE_FLIGHT",
        message="No flight satisfies the passenger constraints.",
        selected_flight=None,
        booking=None,
    )

    check = evaluate_no_flight_selected(
        result=result,
    )

    assert check.name == "no_flight_selected"
    assert check.status == "PASS"


def test_no_booking_created_check_passes_for_qf_002():
    """
    When no eligible flight exists, QForge should expect that
    no booking was created.
    """

    result = RebookingResult(
        status="NO_ELIGIBLE_FLIGHT",
        message="No flight satisfies the passenger constraints.",
        selected_flight=None,
        booking=None,
    )

    check = evaluate_no_booking_created(
        result=result,
    )

    assert check.name == "no_booking_created"
    assert check.status == "PASS"


def test_booking_created_check_uses_verified_state_result():
    """
    This check does not query system state itself.

    It receives the result of state verification and converts
    that boolean into a structured QForge evaluation check.
    """

    check = build_booking_created_check(
        booking_exists=True,
    )

    assert check.name == "booking_created"
    assert check.status == "PASS"