from airline_agent.agents.rebooking_agent import rebook_passenger
from airline_agent.models.rebooking import (
    RebookingRequest,
    RebookingResult,
)

from qforge.scenarios.models import RebookingScenario


class QForgeRunner:

    def run_rebooking_scenario(
        self,
        scenario: RebookingScenario,
    ) -> RebookingResult:

        request = RebookingRequest(
            passenger_id=scenario.passenger_id,
            origin=scenario.origin,
            destination=scenario.destination,
            travel_date=scenario.travel_date,
            arrival_deadline=scenario.arrival_deadline,
            max_additional_cost=scenario.max_additional_cost,
        )

        result = rebook_passenger(request)

        return result