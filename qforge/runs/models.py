from pydantic import BaseModel

from airline_agent.models.rebooking import RebookingResult
from qforge.evaluators.models import EvaluationResult


class TestRunResult(BaseModel):
    """
    Represents one complete QForge scenario execution.

    A test run connects:
    - which scenario was executed,
    - what the System Under Test returned,
    - how QForge evaluated that behavior,
    - and the final PASS / FAIL outcome.

    Later this model can grow to include timestamps,
    duration, environment, model version, and other
    execution metadata.
    """

    run_id: str
    scenario_id: str

    # Raw behavior observed from the System Under Test.
    agent_result: RebookingResult

    # Structured QForge evaluation of that behavior.
    evaluation: EvaluationResult

    # Overall QForge result for the run.
    status: str