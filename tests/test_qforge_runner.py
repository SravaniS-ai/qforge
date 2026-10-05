from qforge.runner import QForgeRunner
from qforge.scenarios.qf_001 import QF_001


def test_qforge_runner_executes_qf_001():

    runner = QForgeRunner()

    result = runner.run_rebooking_scenario(QF_001)

    assert result.status == "CONFIRMED"
    assert result.selected_flight is not None
    assert result.selected_flight.flight_id == "F101"

    assert result.booking is not None
    assert result.booking.flight_id == "F101"