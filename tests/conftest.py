import pytest

from airline_agent.services.airline_service import BOOKINGS


@pytest.fixture(autouse=True)
def reset_booking_state():
    """
    Keep every test independent by resetting the temporary
    in-memory booking store before and after each test.

    QForge currently uses a global BOOKINGS list as temporary
    system state. Without cleanup, a booking created by one test
    could affect later tests and produce misleading results.

    This fixture can be removed or redesigned once booking state
    moves behind a repository/database abstraction.
    """

    # Start every test with a clean booking state.
    BOOKINGS.clear()

    # Give control back to pytest so the actual test can run.
    yield

    # Clean again after the test so no state leaks into another test.
    BOOKINGS.clear()