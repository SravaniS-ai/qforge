import pytest

from qforge.runs.service import execute_test_run
from qforge.scenarios.qf_001 import QF_001
from qforge.scenarios.qf_002 import QF_002
from qforge.scenarios.qf_003 import QF_003


@pytest.mark.parametrize(
    "scenario",
    [
        pytest.param(QF_001, id="QF-001"),
        pytest.param(QF_002, id="QF-002"),
        pytest.param(QF_003, id="QF-003"),
    ],
)
def test_execute_test_run_for_rebooking_scenarios(scenario):
    """
    Verify that the QForge run service can execute different
    rebooking scenarios through the same orchestration flow.

    The scenario itself defines the expected SUT outcome.
    """

    run_result = execute_test_run(
        scenario=scenario,
    )

    # Every run should receive a unique QForge run identifier.
    assert run_result.run_id.startswith("RUN-")

    # The run must remain linked to the scenario that produced it.
    assert run_result.scenario_id == scenario.scenario_id

    # The SUT should return the outcome expected by the scenario.
    assert (
        run_result.agent_result.status
        == scenario.expected_status
    )

    # QForge should consider the observed behavior correct.
    assert run_result.evaluation.status == "PASS"

    # The top-level run status should mirror the evaluation.
    assert run_result.status == "PASS"