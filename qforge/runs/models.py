from datetime import datetime

from pydantic import BaseModel

from airline_agent.models.rebooking import RebookingResult
from qforge.evaluators.models import EvaluationResult


class TestRunResult(BaseModel):
    """
    Represents one complete QForge scenario execution.

    A test run records:
    - which scenario was executed,
    - when execution started and finished,
    - how long the run took,
    - what the System Under Test returned,
    - how QForge evaluated that behavior,
    - and the final PASS / FAIL outcome.

    This gives QForge one structured object that can later
    be persisted, reported, compared, or analyzed.
    """

    # Unique identity for this QForge execution.
    run_id: str

    # Scenario that produced this execution.
    scenario_id: str

    # Run lifecycle metadata.
    started_at: datetime
    finished_at: datetime
    duration_ms: float

    # Raw behavior observed from the System Under Test.
    agent_result: RebookingResult

    # QForge's structured judgment of that behavior.
    evaluation: EvaluationResult

    # Overall result of the complete run.
    status: str