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

def test_index_page_get(client):
    # Test if the index page is accessible via GET request
    response = client.get('/')
    assert response.status_code == 200
    assert b"Weather App" in response.data  # Check if the title is rendered

def test_weather_page_valid_city(client, mocker):
    # Mock the weather API response
    mock_response = {
        "name": "London",
        "main": {"temp": 15},
        "weather": [{"description": "clear sky"}],
    }
    mocker.patch('requests.get', return_value=MockResponse(mock_response, 200))

    # Simulate submitting a valid city name
    response = client.post('/', data={'city': 'London'})
    assert response.status_code == 200
    assert b"Weather in London" in response.data  # Check if the city name is displayed
    assert b"Temperature" in response.data  # Check if temperature is displayed

def test_weather_page_invalid_city(client, mocker):
    # Mock the weather API response for invalid city
    mock_response = {"error": "City not found"}
    mocker.patch('requests.get', return_value=MockResponse(mock_response, 404))

    # Simulate submitting an invalid city name
    response = client.post('/', data={'city': 'InvalidCity'})
    assert response.status_code == 200
    assert b"City not found" in response.data  # Check if error message is displayed

def test_weather_page_empty_city(client):
    # Simulate submitting an empty city name
    response = client.post('/', data={'city': ''})
    assert response.status_code == 200
    assert b"Enter city name" in response.data  # Ensure the message appears for empty input

