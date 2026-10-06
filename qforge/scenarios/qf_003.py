from qforge.scenarios.models import RebookingScenario


QF_003 = RebookingScenario(
    scenario_id="QF-003",
    passenger_id="P125",
    origin="DFW",
    destination="ORD",
    travel_date="2026-10-04",
    arrival_deadline="22:00",
    max_additional_cost=50,
    expected_status="NO_ELIGIBLE_FLIGHT",
    booking_required=False,
)