import pytest
from qforge.evaluators.rebooking_evaluator import evaluate_rebooking
from qforge.runner import QForgeRunner
from qforge.scenarios.qf_001 import QF_001
from qforge.scenarios.qf_002 import QF_002
from qforge.scenarios.qf_003 import QF_003
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