import pytest

from airline_agent.models.booking import (
    BookingRequest,
    BookingResponse,
)
from airline_agent.models.flight import Flight
from airline_agent.models.rebooking import RebookingResult
from airline_agent.services.airline_service import (
    FLIGHTS,
    create_booking,
)

from qforge.evaluators.rebooking_evaluator import evaluate_rebooking
from qforge.runner import QForgeRunner
from qforge.scenarios.qf_001 import QF_001
from qforge.scenarios.qf_002 import QF_002
from qforge.scenarios.qf_003 import QF_003

def get_flight(flight_id: str):
    """
    Return a known test flight from the temporary airline flight store.

    Fault-injection tests use specific flights to create controlled
    defects. Keeping flight lookup in one helper makes those tests
    easier to read and avoids repeating search logic.
    """

    return next(
        flight
        for flight in FLIGHTS
        if flight.flight_id == flight_id
    )

def assert_only_check_failed(evaluation, expected_failed_check):
    """
    Verify that exactly one evaluator check failed.

    Fault-injection tests should isolate one defect at a time.
    If additional checks fail unexpectedly, the test should expose
    that instead of hiding it.
    """

    failed_checks = [
        check.name
        for check in evaluation.checks
        if check.status == "FAIL"
    ]

    assert failed_checks == [expected_failed_check]

def test_qforge_evaluator_detects_fake_booking():

    fake_result = RebookingResult(
        status="CONFIRMED",
        message="Passenger successfully rebooked.",
        selected_flight=Flight(
            flight_id="F101",
            origin="DFW",
            destination="ORD",
            departure_time="15:00",
            arrival_time="18:30",
            additional_cost=120,
            available_seats=5,
        ),
        booking=BookingResponse(
            booking_id="B_FAKE",
            passenger_id="P123",
            flight_id="F101",
            status="CONFIRMED",
        ),
    )

    evaluation = evaluate_rebooking(
        scenario=QF_001,
        result=fake_result,
    )

    assert evaluation.status == "FAIL"

    assert_only_check_failed(
    evaluation,
    "booking_created",
    )

@pytest.mark.parametrize(
    "scenario",
    [
        pytest.param(QF_001, id="QF-001"),
        pytest.param(QF_002, id="QF-002"),
        pytest.param(QF_003, id="QF-003"),
    ],
)
def test_qforge_scenarios_pass(scenario):

    runner = QForgeRunner()

    agent_result = runner.run_rebooking_scenario(scenario)

    evaluation = evaluate_rebooking(
        scenario=scenario,
        result=agent_result,
    )

    assert agent_result.status == scenario.expected_status
    assert evaluation.status == "PASS"

    for check in evaluation.checks:
        assert check.status == "PASS"

def test_qforge_evaluator_detects_late_flight():
    """
    Verify that QForge rejects an agent result when the selected
    flight arrives after the passenger's required deadline.

    We deliberately construct faulty agent behavior here instead
    of modifying the real rebooking agent. This lets us test the
    evaluator independently from the SUT's decision logic.
    """

    # F102 is a real DFW -> ORD flight, but it arrives at 21:00.
    # QF-001 requires arrival by 20:00, so selecting F102 is wrong.
    late_flight = get_flight("F102")

    # Create a REAL booking in system state.
    #
    # This is important because we want this test to isolate only
    # the arrival-time defect. If the booking were fake, QForge
    # would correctly fail multiple checks and we would not know
    # whether arrival validation itself was working.
    booking = create_booking(
        BookingRequest(
            passenger_id=QF_001.passenger_id,
            flight_id=late_flight.flight_id,
        )
    )

    # Simulate a faulty agent claiming that F102 was the correct
    # rebooking decision.
    faulty_result = RebookingResult(
        status="CONFIRMED",
        message="Passenger successfully rebooked.",
        selected_flight=late_flight,
        booking=booking,
    )

    evaluation = evaluate_rebooking(
        scenario=QF_001,
        result=faulty_result,
    )

    # QForge must reject the overall agent behavior.
    assert evaluation.status == "FAIL"

    # Find the specific arrival-deadline evaluation result.
    assert_only_check_failed(
    evaluation,
    "arrival_deadline",
    )

def test_qforge_evaluator_detects_over_budget_flight():
    """
    Verify that QForge rejects an agent result when the selected
    flight exceeds the passenger's maximum allowed additional cost.

    The other conditions are intentionally valid so that this test
    isolates only the cost-constraint defect.
    """

    # F103 arrives before QF-001's 20:00 deadline and goes to ORD,
    # but its additional cost is $250.
    #
    # QF-001 allows a maximum additional cost of $200.
    expensive_flight = get_flight("F103")

    # Create a REAL booking so booking verification itself succeeds.
    # We want QForge to fail because of cost, not because of
    # missing system state.
    booking = create_booking(
        BookingRequest(
            passenger_id=QF_001.passenger_id,
            flight_id=expensive_flight.flight_id,
        )
    )

    # Simulate an agent incorrectly choosing the expensive flight.
    faulty_result = RebookingResult(
        status="CONFIRMED",
        message="Passenger successfully rebooked.",
        selected_flight=expensive_flight,
        booking=booking,
    )

    evaluation = evaluate_rebooking(
        scenario=QF_001,
        result=faulty_result,
    )

    # Since one business constraint is violated,
    # the overall QForge evaluation must fail.
    assert evaluation.status == "FAIL"

    # Extract the specific cost check from the structured result.
    assert_only_check_failed(
    evaluation,
    "cost_constraint",
    )

def test_qforge_evaluator_detects_booking_mismatch():
    """
    Verify that QForge detects a consistency error where the agent
    selects one flight but the booking is created for another flight.

    This simulates an agent/tool-orchestration defect:
    the decision and the action do not match.
    """

    # F101 is a valid flight for QF-001 and will be presented as
    # the flight the agent claims to have selected.
    selected_flight = get_flight("F101")

    # Create a REAL booking for a different flight.
    #
    # The booking itself exists in system state, so the
    # booking_created check should still pass.
    wrong_booking = create_booking(
        BookingRequest(
            passenger_id=QF_001.passenger_id,
            flight_id="F103",
        )
    )

    # Simulate faulty agent behavior:
    #
    # Agent says:
    #   selected flight = F101
    #
    # Actual booking:
    #   booked flight = F103
    faulty_result = RebookingResult(
        status="CONFIRMED",
        message="Passenger successfully rebooked.",
        selected_flight=selected_flight,
        booking=wrong_booking,
    )

    evaluation = evaluate_rebooking(
        scenario=QF_001,
        result=faulty_result,
    )

    # The overall behavior must be rejected.
    assert evaluation.status == "FAIL"

    # Extract the consistency check that compares the agent's
    # selected flight with the flight actually booked.
    assert_only_check_failed(
    evaluation,
    "booking_matches_selected_flight",
    )

def test_qforge_evaluator_detects_unexpected_status():
    """
    Verify that QForge detects when the agent reports an unexpected
    overall status, even if the selected flight and booking are valid.

    This isolates status validation from all other business checks.
    """

    # F101 is a valid flight for QF-001.
    selected_flight = next(
        flight
        for flight in FLIGHTS
        if flight.flight_id == "F101"
    )

    # Create a REAL booking so all state-related checks can pass.
    booking = create_booking(
        BookingRequest(
            passenger_id=QF_001.passenger_id,
            flight_id=selected_flight.flight_id,
        )
    )

    # Simulate inconsistent agent behavior:
    #
    # The agent actually selected and booked a valid flight,
    # but reports the wrong high-level outcome.
    faulty_result = RebookingResult(
        status="NO_ELIGIBLE_FLIGHT",
        message="No eligible flight was found.",
        selected_flight=selected_flight,
        booking=booking,
    )

    evaluation = evaluate_rebooking(
        scenario=QF_001,
        result=faulty_result,
    )

    # Overall evaluation must fail because the reported status
    # does not match QF-001's expected outcome.
    assert evaluation.status == "FAIL"

    # Find the specific status validation result.
    assert_only_check_failed(
    evaluation,
    "status",
    )