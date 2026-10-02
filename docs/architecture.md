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

