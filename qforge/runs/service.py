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

    This function coordinates the major steps of a run:

    1. Execute the scenario against the System Under Test.
    2. Capture the observed agent result.
    3. Evaluate that result against the scenario expectations.
    4. Package everything into one TestRunResult.

    The function coordinates the workflow, but it does not
    implement agent logic or evaluation rules itself.
    """

    # The runner is responsible only for executing the scenario
    # against the System Under Test.
    runner = QForgeRunner()

    agent_result = runner.run_rebooking_scenario(
        scenario=scenario,
    )

    # The evaluator compares the observed SUT behavior with the
    # expected behavior defined by the QForge scenario.
    evaluation = evaluate_rebooking(
        scenario=scenario,
        result=agent_result,
    )

    # Each run needs a unique identity so that results can later
    # be stored, retrieved, compared, or included in reports.
    run_id = f"RUN-{uuid4().hex[:8].upper()}"

    # Package the entire execution into a single platform object.
    return TestRunResult(
        run_id=run_id,
        scenario_id=scenario.scenario_id,
        agent_result=agent_result,
        evaluation=evaluation,
        status=evaluation.status,
    )