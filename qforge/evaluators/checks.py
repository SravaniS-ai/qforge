from airline_agent.models.rebooking import RebookingResult

from qforge.evaluators.models import EvaluationCheck
from qforge.scenarios.models import RebookingScenario


def evaluate_status(
    scenario: RebookingScenario,
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Verify that the SUT returned the overall status expected
    by the executable QForge scenario.

    Example:
        expected = CONFIRMED
        observed = CONFIRMED
        result   = PASS
    """

    passed = result.status == scenario.expected_status

    return EvaluationCheck(
        name="status",
        status="PASS" if passed else "FAIL",
        reason=(
            "Agent returned the expected status."
            if passed
            else (
                f"Expected status {scenario.expected_status}, "
                f"but received {result.status}."
            )
        ),
    )


def evaluate_destination(
    scenario: RebookingScenario,
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Verify that the flight selected by the agent reaches
    the destination required by the scenario.
    """

    selected_flight = result.selected_flight

    passed = (
        selected_flight is not None
        and selected_flight.destination == scenario.destination
    )

    return EvaluationCheck(
        name="destination",
        status="PASS" if passed else "FAIL",
        reason=(
            "Selected flight has the correct destination."
            if passed
            else "Selected flight destination is incorrect or missing."
        ),
    )


def evaluate_arrival_deadline(
    scenario: RebookingScenario,
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Verify that the selected flight arrives on or before
    the passenger's required arrival deadline.
    """

    selected_flight = result.selected_flight

    passed = (
        selected_flight is not None
        and selected_flight.arrival_time
        <= scenario.arrival_deadline
    )

    return EvaluationCheck(
        name="arrival_deadline",
        status="PASS" if passed else "FAIL",
        reason=(
            "Selected flight arrives within the deadline."
            if passed
            else "Selected flight arrives after the deadline or is missing."
        ),
    )


def evaluate_cost_constraint(
    scenario: RebookingScenario,
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Verify that the selected flight does not exceed the
    maximum additional cost allowed by the scenario.
    """

    selected_flight = result.selected_flight

    passed = (
        selected_flight is not None
        and selected_flight.additional_cost
        <= scenario.max_additional_cost
    )

    return EvaluationCheck(
        name="cost_constraint",
        status="PASS" if passed else "FAIL",
        reason=(
            "Selected flight satisfies the cost constraint."
            if passed
            else "Selected flight exceeds the allowed cost or is missing."
        ),
    )


def evaluate_booking_match(
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Verify cross-object consistency.

    The flight the agent claims it selected must be the same
    flight that was actually recorded in the booking response.
    """

    selected_flight = result.selected_flight

    passed = (
        selected_flight is not None
        and result.booking is not None
        and result.booking.flight_id == selected_flight.flight_id
    )

    return EvaluationCheck(
        name="booking_matches_selected_flight",
        status="PASS" if passed else "FAIL",
        reason=(
            "Booked flight matches the selected flight."
            if passed
            else "Booked flight does not match the selected flight."
        ),
    )


def evaluate_no_flight_selected(
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Used when the scenario expects NO_ELIGIBLE_FLIGHT.

    In that situation, selecting no flight is correct behavior.
    """

    passed = result.selected_flight is None

    return EvaluationCheck(
        name="no_flight_selected",
        status="PASS" if passed else "FAIL",
        reason=(
            "No flight was selected, as expected."
            if passed
            else "A flight was selected when none should have been."
        ),
    )


def evaluate_no_booking_created(
    result: RebookingResult,
) -> EvaluationCheck:
    """
    Used when the scenario expects no valid rebooking.

    If no flight should be selected, the agent should also
    avoid creating a booking.
    """

    passed = result.booking is None

    return EvaluationCheck(
        name="no_booking_created",
        status="PASS" if passed else "FAIL",
        reason=(
            "No booking was created, as expected."
            if passed
            else "A booking was created when none should have been."
        ),
    )


def build_booking_created_check(
    booking_exists: bool,
) -> EvaluationCheck:
    """
    Convert the result of system-state verification into a
    structured QForge evaluation check.

    The actual lookup of booking state intentionally remains
    outside this function for now. Later, a state-verification
    abstraction will replace direct access to the BOOKINGS list.
    """

    return EvaluationCheck(
        name="booking_created",
        status="PASS" if booking_exists else "FAIL",
        reason=(
            "Booking exists in actual system state."
            if booking_exists
            else "Agent reported a booking, but no matching booking exists."
        ),
    )