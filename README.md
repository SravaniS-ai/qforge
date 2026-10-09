# QForge

QForge is an AI Quality Engineering platform for evaluating the behavior of AI-enabled systems.

The current System Under Test (SUT) is an Airline Rebooking Agent.

QForge verifies not only what the agent says, but also whether the agent's decisions satisfy business constraints and whether claimed actions actually occurred in system state.

## What QForge Validates

QForge currently checks:

- Expected agent status
- Destination correctness
- Arrival deadline constraints
- Maximum additional cost
- Whether a booking was actually created
- Whether the booked flight matches the selected flight
- Expected no-result behavior when no eligible flight exists

## Architecture

```text
Executable Scenario
        ↓
QForge Runner
        ↓
Airline Rebooking Agent
        ↓
Airline Services
        ↓
Observed Result
        ↓
QForge Evaluator
        ↓
Structured PASS / FAIL
```

## Example Scenario

```text
QF-001

Origin: DFW
Destination: ORD
Arrival deadline: 20:00
Maximum additional cost: $200

Expected result:
CONFIRMED
```

Available flights:

```text
F101 → arrives 18:30 → $120 → eligible
F102 → arrives 21:00 → $80  → too late
F103 → arrives 19:15 → $250 → too expensive
```

Expected QForge result:

```text
status                           PASS
destination                      PASS
arrival_deadline                 PASS
cost_constraint                  PASS
booking_created                  PASS
booking_matches_selected_flight  PASS

Overall: PASS
```

## Fault Injection

QForge is also tested against deliberately faulty agent behavior.

Examples:

```text
Late flight
→ arrival_deadline FAIL

Over-budget flight
→ cost_constraint FAIL

Fake booking
→ booking_created FAIL

Selected flight != booked flight
→ booking_matches_selected_flight FAIL

Unexpected status
→ status FAIL
```

This proves that QForge does not only pass correct behavior — it can also detect and diagnose incorrect behavior.

## Current Scenarios

- `QF-001` — successful rebooking
- `QF-002` — no flight meets the arrival deadline
- `QF-003` — no flight meets the budget constraint

## Technology Stack

- Python
- FastAPI
- Pydantic
- Pytest
- Uvicorn
- HTTPX
- Git
- GitHub

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
python -m uvicorn airline_agent.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Run tests:

```bash
python -m pytest -v
```

## Current Scope

The current version intentionally uses a simple in-memory implementation.

The following are deferred until the architecture creates a real need:

- PostgreSQL
- Redis
- Kafka
- Celery
- Distributed workers
- Docker/Kubernetes
- AWS infrastructure

## Design Principle

Build the simplest architecture that correctly solves the current problem.

Add complexity only when a real requirement justifies it.
