# QForge Architecture

## 1. Purpose

QForge is an AI Quality Engineering platform used to evaluate the behavior of an AI-enabled system.

The current System Under Test (SUT) is an Airline Rebooking Agent.

QForge does not simply check whether the agent returns a plausible response. It verifies whether the agent's decisions satisfy business constraints and whether claimed actions actually occurred in system state.

---

## 2. High-Level Architecture

```text
Executable Scenario
        ↓
QForge Runner
        ↓
System Under Test
        ↓
Observed Result
        ↓
QForge Evaluator
        ↓
Structured Evaluation Result
        ↓
PASS / FAIL
```

The System Under Test currently contains:

```text
FastAPI Layer
      ↓
Rebooking Agent
      ↓
Airline Services
      ↓
In-Memory System State
```

---

## 3. System Boundary

### QForge owns

- Scenario definitions
- Expected outcomes
- Scenario execution
- Evaluation rules
- PASS / FAIL decisions
- Failure diagnostics

### Airline Rebooking System owns

- Flight data
- Flight search
- Rebooking decisions
- Booking creation
- Booking state
- API endpoints

Keeping these responsibilities separate prevents test-specific behavior from leaking into the production system.

---

## 4. Airline Rebooking System

### API Layer

File:

```text
airline_agent/main.py
```

Responsibilities:

- Expose HTTP endpoints
- Accept validated requests
- Delegate work to services or agent logic
- Return API responses

The API layer should not contain core business logic.

---

### Rebooking Agent

File:

```text
airline_agent/agents/rebooking_agent.py
```

Responsibilities:

- Coordinate the rebooking workflow
- Search available flights
- Apply passenger constraints
- Select an eligible flight
- Request booking creation

Current implementation is deterministic and rule-based.

This deterministic baseline gives QForge a known reference behavior before introducing LLM-based decision making later.

---

### Airline Service Layer

File:

```text
airline_agent/services/airline_service.py
```

Responsibilities:

- Search flights
- Validate requested flights
- Create bookings
- Maintain temporary in-memory system state

Current state is represented using:

```python
FLIGHTS = [...]
BOOKINGS = []
```

This is intentionally temporary.

Later versions will place persistence behind a repository or database abstraction.

---

### Models

Location:

```text
airline_agent/models/
```

Responsibilities:

- Define request and response contracts
- Validate data using Pydantic
- Provide consistent data structures between layers

Examples:

- `Flight`
- `FlightSearchRequest`
- `BookingRequest`
- `BookingResponse`
- `RebookingRequest`
- `RebookingResult`

---

## 5. QForge Platform

### Scenarios

Location:

```text
qforge/scenarios/
```

A scenario is a machine-readable executable requirement.

A scenario contains:

- Test input
- Passenger constraints
- Expected system outcome

Example:

```text
QF-001

Origin: DFW
Destination: ORD
Arrival deadline: 20:00
Maximum additional cost: $200

Expected status:
CONFIRMED

Booking required:
True
```

Current scenarios include:

- `QF-001` — successful rebooking
- `QF-002` — no flight meets arrival deadline
- `QF-003` — no flight meets budget constraint

---

### QForge Runner

File:

```text
qforge/runner.py
```

Responsibilities:

- Accept a QForge scenario
- Convert it into an SUT request
- Execute the rebooking workflow
- Capture the observed result

The runner executes behavior.

It does not decide whether that behavior is correct.

---

### QForge Evaluator

Location:

```text
qforge/evaluators/
```

Responsibilities:

- Compare expected behavior with observed behavior
- Validate business constraints
- Validate system state
- Produce structured diagnostics
- Determine overall PASS / FAIL

Current checks include:

```text
status
destination
arrival_deadline
cost_constraint
booking_created
booking_matches_selected_flight
```

For scenarios where no eligible flight is expected, the evaluator instead verifies:

```text
status
no_flight_selected
no_booking_created
```

---

## 6. Expected vs Observed

The core evaluation pattern is:

```text
Expected behavior
        vs
Observed behavior
```

Examples:

```text
Expected destination
vs
Selected flight destination
```

```text
Expected arrival deadline
vs
Selected flight arrival time
```

```text
Expected maximum cost
vs
Selected flight additional cost
```

---

## 7. State Verification

QForge does not trust agent output alone.

For example:

```text
Agent claims:
Booking B9001 was created
```

QForge also checks:

```text
Actual booking state:
Does B9001 really exist?
```

If the agent claims a booking exists but the system state does not contain that booking:

```text
booking_created = FAIL
```

This is important for validating AI agents that may produce plausible output without successfully completing the real action.

---

## 8. Fault Injection

QForge is tested using deliberately faulty agent results.

Current injected defects include:

```text
Late flight
→ arrival_deadline FAIL

Over-budget flight
→ cost_constraint FAIL

Fake booking
→ booking_created FAIL

Selected flight differs from booked flight
→ booking_matches_selected_flight FAIL

Unexpected agent status
→ status FAIL
```

Each fault-injection test attempts to isolate one defect so QForge can prove that it fails for the correct reason.

---

## 9. Test Isolation

Booking state is currently stored in a global in-memory list.

Pytest uses an automatic fixture to clear booking state before and after each test.

This prevents one test from affecting another.

```text
Test A
→ clean state
→ execute
→ cleanup

Test B
→ clean state
→ execute
→ cleanup
```

---

## 10. Current Technology Stack

- Python
- FastAPI
- Pydantic
- Pytest
- Uvicorn
- HTTPX
- Git
- GitHub

---

## 11. Deferred Architecture

The following technologies are intentionally not part of the first version:

- PostgreSQL
- Redis
- Kafka
- Celery
- Background workers
- Distributed workers
- Docker/Kubernetes
- AWS infrastructure

These will be introduced only when QForge develops requirements that justify them.

---

## 12. Current Architecture Principle

Build the simplest architecture that correctly solves the current problem.

Add complexity only when a real requirement creates the need for it.
