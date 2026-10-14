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

        # Lifecycle timestamps should be recorded for every run.
    assert run_result.started_at is not None
    assert run_result.finished_at is not None

    # A run cannot logically finish before it starts.
    assert run_result.finished_at >= run_result.started_at

    # Duration should always be non-negative.
    assert run_result.duration_ms >= 0

def test_same_scenario_creates_distinct_run_ids():
    """
    Verify that executing the same scenario twice produces
    two separate QForge run records.

    The scenario identity can stay the same, but every execution
    must have its own run_id.
    """

    first_run = execute_test_run(
        scenario=QF_001,
    )

    second_run = execute_test_run(
        scenario=QF_001,
    )

    # Both executions belong to the same scenario.
    assert first_run.scenario_id == "QF-001"
    assert second_run.scenario_id == "QF-001"

    # But they must represent different run instances.
    assert first_run.run_id != second_run.run_id

    # Both runs should still evaluate successfully.
    assert first_run.status == "PASS"
    assert second_run.status == "PASS"