# QForge Architecture

## 1. System Boundary

QForge is the AI Quality Engineering platform.

The Airline Rebooking Agent is the System Under Test (SUT).

```text
QForge
│
├── Test Scenario
├── Test Runner
├── Evaluators
└── Results

        │
        │ tests
        ▼

System Under Test (SUT)
│
└── Airline Rebooking Agent
     │
     ├── Flight Search API
     └── Booking API
```

---

## 2. Component Responsibilities

### Test Scenario

Defines:

- passenger situation
- test input
- business constraints
- expected outcome

Example:

```text
Destination: Chicago
Arrival deadline: 8:00 PM
Maximum additional cost: $200
```

### Test Runner

The Test Runner:

- loads a test scenario
- sends the request to the Rebooking Agent
- captures the agent response
- captures API or tool calls
- sends execution data to the evaluators

### Evaluators

Evaluators verify whether the AI agent behaved correctly.

Examples:

- Was the correct destination selected?
- Was the arrival deadline satisfied?
- Was the cost constraint satisfied?
- Did the selected flight exist?
- Was the Booking API called?
- Were the correct arguments passed?
- Was a booking actually created?
- Does the final response match the actual system state?

### Results

Stores the final evaluation outcome.

Initial statuses:

```text
PASS
FAIL
WARN
```

---

## 3. Airline System Components

### Rebooking Agent

The Rebooking Agent is the AI application being tested.

Its responsibilities are:

1. Understand the passenger request.
2. Call the Flight Search API.
3. Review available flights.
4. Apply passenger-specific constraints.
5. Select an eligible flight.
6. Call the Booking API.
7. Return the result to the passenger.

### Flight Search API

The Flight Search API:

- searches available flights
- returns route information
- returns departure and arrival times
- returns additional cost
- returns seat availability

It does not decide which flight is best for the passenger.

### Booking API

The Booking API:

- validates that the flight exists
- checks seat availability
- creates the booking
- returns booking confirmation

It does not decide whether the selected flight satisfies passenger preferences.

---

## 4. Initial Data Flow

```text
Test Scenario
     │
     ▼
QForge Test Runner
     │
     ▼
Rebooking Agent
     │
     ▼
Flight Search API
     │
     ▼
Available Flights
     │
     ▼
Rebooking Agent
     │
     │ applies passenger constraints
     ▼
Booking API
     │
     ▼
Booking Confirmation
     │
     ▼
Rebooking Agent
     │
     ▼
Agent Response
     │
     ▼
QForge Evaluators
     │
     ▼
PASS / FAIL / WARN
```

---

## 5. QF-001 Example

Passenger requirements:

```text
Destination: Chicago
Arrival deadline: 8:00 PM
Maximum additional cost: $200
```

Available flights:

```text
F101 -> Chicago -> 6:30 PM -> $120
F102 -> Chicago -> 9:00 PM -> $80
F103 -> Chicago -> 7:15 PM -> $250
```

The Rebooking Agent should select:

```text
F101
```

because:

```text
F101
Arrival before 8 PM: YES
Cost <= $200: YES
Eligible: YES

F102
Arrival before 8 PM: NO
Eligible: NO

F103
Arrival before 8 PM: YES
Cost <= $200: NO
Eligible: NO
```

---

## 6. Key Design Principle

QForge validates what the AI system actually did, not only what the AI system said.

Example:

```text
Agent response:
"Your flight has been successfully booked."

Actual system state:
No booking exists.

QForge result:
FAIL
```

---

## 7. Current Scope

Month 1 is intentionally simple.

Current technologies:

```text
Python
FastAPI
Pydantic
Pytest
Mock Airline APIs
JSON Results
Git / GitHub
```

Deferred until later:

```text
PostgreSQL
Redis
Background Workers
Celery
Kafka
AWS
Distributed Processing
Kubernetes
Advanced Observability
```

These will be introduced when QForge develops a real architectural need for them.
