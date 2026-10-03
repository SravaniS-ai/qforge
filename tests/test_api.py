from fastapi.testclient import TestClient

from airline_agent.main import app

client = TestClient(app)


def test_search_flights():
    response = client.post(
        "/flights/search",
        json={
            "origin": "DFW",
            "destination": "ORD",
            "travel_date": "2026-10-04",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "flights" in data
    assert len(data["flights"]) == 3


def test_create_booking():
    response = client.post(
        "/bookings",
        json={
            "passenger_id": "P123",
            "flight_id": "F101",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["passenger_id"] == "P123"
    assert data["flight_id"] == "F101"
    assert data["status"] == "CONFIRMED"


def test_booking_invalid_flight():
    response = client.post(
        "/bookings",
        json={
            "passenger_id": "P123",
            "flight_id": "F999",
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"]["error"] == "FLIGHT_NOT_FOUND"