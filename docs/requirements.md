# QForge Requirements

## QF-001 — Cancelled Flight Rebooking

### Given
A passenger's original flight has been cancelled.

### Passenger Requirements
- Destination: Chicago
- Arrival deadline: 8:00 PM
- Maximum additional cost: $200

### Expected Agent Behavior
1. Search available flights.
2. Consider only flights going to Chicago.
3. Reject flights arriving after 8:00 PM.
4. Reject flights costing more than $200 extra.
5. Select an eligible flight.
6. Call the booking API.
7. Return the confirmed itinerary.

### QForge Validation
QForge must verify:
- The selected destination is Chicago.
- The selected flight arrives by 8:00 PM.
- Additional cost is no more than $200.
- The selected flight actually exists.
- The correct booking tool/API was called.
- Correct arguments were sent to the booking API.
- A real booking was created.
- The final AI response matches the actual system state.