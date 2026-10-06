from datetime import date, time

from pydantic import BaseModel, Field


class RebookingScenario(BaseModel):
    scenario_id: str

    passenger_id: str
    origin: str
    destination: str
    travel_date: date

    arrival_deadline: time
    max_additional_cost: float = Field(ge=0)

    expected_status: str
    booking_required: bool = True