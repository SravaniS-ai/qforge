# QForge API Contracts

This document defines how the Airline Rebooking Agent communicates with the airline APIs.

---

## 1. Flight Search API

### Purpose

The Flight Search API returns available flights for a requested route and travel date.

### Endpoint

```text
POST /flights/search
```

### Request

```json
{
  "origin": "DFW",
  "destination": "ORD",
  "travel_date": "2026-10-04"
}
```

### Request Fields

- `origin` — departure airport code
- `destination` — arrival airport code
- `travel_date` — requested travel date

### Success Response

```json
{
  "flights": [
    {
      "flight_id": "F101",
      "origin": "DFW",
      "destination": "ORD",
      "departure_time": "15:00",
      "arrival_time": "18:30",
      "additional_cost": 120,
      "available_seats": 5
    },
    {
      "flight_id": "F102",
      "origin": "DFW",
      "destination": "ORD",
      "departure_time": "17:30",
      "arrival_time": "21:00",
      "additional_cost": 80,
      "available_seats": 7
    },
    {
      "flight_id": "F103",
      "origin": "DFW",
      "destination": "ORD",
      "departure_time": "16:00",
      "arrival_time": "19:15",
      "additional_cost": 250,
      "available_seats": 3
    }
  ]
}
```

### Responsibilities

The Flight Search API:

- searches available flights
- returns route information
- returns departure and arrival times
- returns additional cost
- returns seat availability
- does not decide which flight is best for the passenger

### Example Error Response

```json
{
  "error": "NO_FLIGHTS_FOUND",
  "message": "No flights were found for the requested route and date."
}
```

---

## 2. Booking API

### Purpose

The Booking API creates a booking for a passenger on a selected flight.

### Endpoint

```text
POST /bookings
```

### Request

```json
{
  "passenger_id": "P123",
  "flight_id": "F101"
}
```

### Request Fields

- `passenger_id` — identifies the passenger
- `flight_id` — identifies the flight to book

### Success Response

```json
{
  "booking_id": "B9001",
  "passenger_id": "P123",
  "flight_id": "F101",
  "status": "CONFIRMED"
}
```

### Responsibilities

The Booking API:

- validates that the flight exists
- checks seat availability
- creates the booking
- returns booking confirmation

### Example Error: Flight Not Found

```json
{
  "error": "FLIGHT_NOT_FOUND",
  "message": "Flight F999 does not exist."
}
```

### Example Error: No Seats Available

```json
{
  "error": "NO_SEATS_AVAILABLE",
  "message": "No seats are available for flight F101."
}
```

---

## 3. Responsibility Boundary

The APIs provide data and perform airline operations.

The Rebooking Agent is responsible for applying passenger-specific rules.

For QF-001:

```text
Destination = Chicago
Arrival deadline <= 8:00 PM
Additional cost <= $200
```

The Flight Search API does not apply these decision rules.

The Booking API does not apply these decision rules.

The Rebooking Agent evaluates the available flights and selects an eligible flight.
