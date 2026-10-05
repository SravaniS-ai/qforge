from pydantic import BaseModel


class EvaluationCheck(BaseModel):
    name: str
    status: str
    reason: str


class EvaluationResult(BaseModel):
    scenario_id: str
    status: str
    checks: list[EvaluationCheck]