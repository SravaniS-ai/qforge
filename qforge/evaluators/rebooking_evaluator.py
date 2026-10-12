from airline_agent.models.rebooking import RebookingResult
from airline_agent.services.airline_service import BOOKINGS

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
from qforge.evaluators.models import EvaluationResult
from qforge.scenarios.models import RebookingScenario


def evaluate_rebooking(
    scenario: RebookingScenario,
    result: RebookingResult,
) -> EvaluationResult:
    """
    Evaluate the observed rebooking result against the behavior
    expected by a QForge scenario.

    This function now acts mainly as an orchestration layer:
    it decides which reusable checks apply to the scenario,
    collects their results, and calculates the overall status.
    """

    checks = []

    # Every scenario should first confirm that the SUT returned
    # the high-level status expected by the executable scenario.
    checks.append(
        evaluate_status(
            scenario=scenario,
            result=result,
        )
    )

    # Successful rebooking scenarios require validation of the
    # selected flight, business constraints, and booking state.
    if scenario.expected_status == "CONFIRMED":

        checks.append(
            evaluate_destination(
                scenario=scenario,
                result=result,
            )
        )

        checks.append(
            evaluate_arrival_deadline(
                scenario=scenario,
                result=result,
            )
        )

        checks.append(
            evaluate_cost_constraint(
                scenario=scenario,
                result=result,
            )
        )

        # Temporary state verification.
        #
        # QForge still reads the SUT's in-memory BOOKINGS list
        # directly. This is known technical debt and will later
        # be replaced by a state-verification abstraction.
        booking_exists = False

        if result.booking is not None:
            booking_exists = any(
                booking.booking_id == result.booking.booking_id
                for booking in BOOKINGS
            )

        checks.append(
            build_booking_created_check(
                booking_exists=booking_exists,
            )
        )

        checks.append(
            evaluate_booking_match(
                result=result,
            )
        )

    # When no valid rebooking is expected, the correct behavior
    # is to avoid selecting a flight and avoid creating a booking.
    elif scenario.expected_status == "NO_ELIGIBLE_FLIGHT":

        checks.append(
            evaluate_no_flight_selected(
                result=result,
            )
        )

        checks.append(
            evaluate_no_booking_created(
                result=result,
            )
        )

    # The overall scenario passes only when every individual
    # evaluation rule passes.
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