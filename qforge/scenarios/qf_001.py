from qforge.scenarios.models import RebookingScenario


QF_001 = RebookingScenario(
    scenario_id="QF-001",
    passenger_id="P123",
    origin="DFW",
    destination="ORD",
    travel_date="2026-10-04",
    arrival_deadline="20:00",
    max_additional_cost=200,
    expected_status="CONFIRMED",
    booking_required=True,
)