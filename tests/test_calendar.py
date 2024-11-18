import pytest
from app import app  # Import the Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_calendar_view(client):
    response = client.get('/calendar')
    assert response.status_code == 200
    assert b"Calendar" in response.data  # Ensure calendar page renders
    assert b"Mon" in response.data  # Check if days of the week are displayed
    assert b"today" in response.data  # Ensure "today" is marked correctly