from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from qforge.evaluators.rebooking_evaluator import evaluate_rebooking
from qforge.runner import QForgeRunner
from qforge.runs.models import TestRunResult
from qforge.scenarios.models import RebookingScenario


def execute_test_run(
    scenario: RebookingScenario,
) -> TestRunResult:
    """
    Execute one complete QForge test run.

    This orchestration service is responsible for:
    - recording run lifecycle metadata,
    - executing the scenario against the SUT,
    - evaluating the observed result,
    - and packaging everything into TestRunResult.

    It does not contain agent decision logic or evaluator rules.
    """

    # Record the wall-clock start time for reporting and persistence.
    #
    # We use UTC so timestamps remain consistent across machines,
    # environments, CI systems, and future distributed workers.
    started_at = datetime.now(timezone.utc)

    # perf_counter() is used specifically for elapsed-time measurement.
    #
    # It is monotonic, which means it is not affected by system-clock
    # adjustments while the test run is executing.
    timer_start = perf_counter()

    # Execute the scenario against the System Under Test.
    runner = QForgeRunner()

    agent_result = runner.run_rebooking_scenario(
        scenario=scenario,
    )

    # Evaluate the SUT behavior against the scenario expectations.
    evaluation = evaluate_rebooking(
        scenario=scenario,
        result=agent_result,
    )

    # Capture elapsed execution time in milliseconds.
    duration_ms = (perf_counter() - timer_start) * 1000

    # Record the wall-clock finish time separately from duration.
    finished_at = datetime.now(timezone.utc)

    # Generate an identifier for this individual execution.
    run_id = f"RUN-{uuid4().hex[:8].upper()}"

    # Package execution, evaluation, and lifecycle metadata into
    # one first-class QForge run record.
    return TestRunResult(
        run_id=run_id,
        scenario_id=scenario.scenario_id,
        started_at=started_at,
        finished_at=finished_at,
        duration_ms=duration_ms,
        agent_result=agent_result,
        evaluation=evaluation,
        status=evaluation.status,
    )