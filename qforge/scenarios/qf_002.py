from qforge.scenarios.models import RebookingScenario


QF_002 = RebookingScenario(
    scenario_id="QF-002",
    passenger_id="P124",
    origin="DFW",
    destination="ORD",
    travel_date="2026-10-04",
    arrival_deadline="17:00",
    max_additional_cost=200,
    expected_status="NO_ELIGIBLE_FLIGHT",
    booking_required=False,
)