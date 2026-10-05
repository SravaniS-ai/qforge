from qforge.evaluators.rebooking_evaluator import evaluate_rebooking
from qforge.runner import QForgeRunner
from qforge.scenarios.qf_001 import QF_001


def test_qforge_evaluator_passes_qf_001():

    runner = QForgeRunner()

    agent_result = runner.run_rebooking_scenario(QF_001)

    evaluation = evaluate_rebooking(
        scenario=QF_001,
        result=agent_result,
    )

    assert evaluation.status == "PASS"

    for check in evaluation.checks:
        assert check.status == "PASS"


from airline_agent.models.booking import BookingResponse
from airline_agent.models.flight import Flight
from airline_agent.models.rebooking import RebookingResult


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

    booking_check = next(
        check
        for check in evaluation.checks
        if check.name == "booking_created"
    )

    assert booking_check.status == "FAIL"