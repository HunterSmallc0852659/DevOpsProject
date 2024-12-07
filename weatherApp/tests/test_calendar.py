import sys
import os
import pytest

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from weatherApp.app import app 

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_calendar_view(client):
    # Test if the /calendar route is accessible
    response = client.get('/calendar')
    assert response.status_code == 200
    assert b"Calendar" in response.data  # Check if the page title is rendered
    assert b"Mon" in response.data  # Check if day labels are present
    assert b"today" in response.data  # Check if "today" is marked
