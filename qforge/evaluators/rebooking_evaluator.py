from airline_agent.models.rebooking import RebookingResult
from airline_agent.services.airline_service import BOOKINGS

from qforge.evaluators.models import (
    EvaluationCheck,
    EvaluationResult,
)
from qforge.scenarios.models import RebookingScenario


def evaluate_rebooking(
    scenario: RebookingScenario,
    result: RebookingResult,
) -> EvaluationResult:

    checks = []

    # 1. Status check
    status_passed = result.status == scenario.expected_status

    checks.append(
        EvaluationCheck(
            name="status",
            status="PASS" if status_passed else "FAIL",
            reason=(
                "Agent returned the expected status."
                if status_passed
                else (
                    f"Expected status {scenario.expected_status}, "
                    f"but received {result.status}."
                )
            ),
        )
    )

    # Successful rebooking scenario
    if scenario.expected_status == "CONFIRMED":

        selected_flight = result.selected_flight

        # 2. Destination check
        destination_passed = (
            selected_flight is not None
            and selected_flight.destination == scenario.destination
        )

        checks.append(
            EvaluationCheck(
                name="destination",
                status="PASS" if destination_passed else "FAIL",
                reason=(
                    "Selected flight has the correct destination."
                    if destination_passed
                    else "Selected flight destination is incorrect or missing."
                ),
            )
        )

        # 3. Arrival deadline check
        arrival_passed = (
            selected_flight is not None
            and selected_flight.arrival_time <= scenario.arrival_deadline
        )

        checks.append(
            EvaluationCheck(
                name="arrival_deadline",
                status="PASS" if arrival_passed else "FAIL",
                reason=(
                    "Selected flight arrives within the deadline."
                    if arrival_passed
                    else "Selected flight arrives after the deadline or is missing."
                ),
            )
        )

        # 4. Cost check
        cost_passed = (
            selected_flight is not None
            and selected_flight.additional_cost
            <= scenario.max_additional_cost
        )

        checks.append(
            EvaluationCheck(
                name="cost_constraint",
                status="PASS" if cost_passed else "FAIL",
                reason=(
                    "Selected flight satisfies the cost constraint."
                    if cost_passed
                    else "Selected flight exceeds the allowed cost or is missing."
                ),
            )
        )

        # 5. Booking actually exists
        booking_exists = False

        if result.booking is not None:
            booking_exists = any(
                booking.booking_id == result.booking.booking_id
                for booking in BOOKINGS
            )

        checks.append(
            EvaluationCheck(
                name="booking_created",
                status="PASS" if booking_exists else "FAIL",
                reason=(
                    "Booking exists in actual system state."
                    if booking_exists
                    else "Agent reported a booking, but no matching booking exists."
                ),
            )
        )

        # 6. Booking matches selected flight
        booking_matches_flight = (
            selected_flight is not None
            and result.booking is not None
            and result.booking.flight_id == selected_flight.flight_id
        )

        checks.append(
            EvaluationCheck(
                name="booking_matches_selected_flight",
                status="PASS" if booking_matches_flight else "FAIL",
                reason=(
                    "Booked flight matches the selected flight."
                    if booking_matches_flight
                    else "Booked flight does not match the selected flight."
                ),
            )
        )

    # No eligible flight scenario
    elif scenario.expected_status == "NO_ELIGIBLE_FLIGHT":

        no_selected_flight = result.selected_flight is None

        checks.append(
            EvaluationCheck(
                name="no_flight_selected",
                status="PASS" if no_selected_flight else "FAIL",
                reason=(
                    "No flight was selected, as expected."
                    if no_selected_flight
                    else "A flight was selected when none should have been."
                ),
            )
        )

        no_booking = result.booking is None

        checks.append(
            EvaluationCheck(
                name="no_booking_created",
                status="PASS" if no_booking else "FAIL",
                reason=(
                    "No booking was created, as expected."
                    if no_booking
                    else "A booking was created when none should have been."
                ),
            )
        )

    overall_status = (
        "PASS"
        if all(check.status == "PASS" for check in checks)
        else "FAIL"
    )

    return EvaluationResult(
        scenario_id=scenario.scenario_id,
        status=overall_status,
        checks=checks,
    )