import pytest
from weatherApp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_weather_page_valid_city(client):
    # Simulate submitting a valid city name
    response = client.post('/', data={'city': 'London'})
    assert response.status_code == 200
    assert b"Weather in London" in response.data  # Check if the city name appears in the response
    assert b"Temperature" in response.data  # Check if temperature data appears

def test_weather_page_invalid_city(client):
    # Simulate submitting an invalid city name
    response = client.post('/', data={'city': 'InvalidCity'})
    assert response.status_code == 200
    assert b"City not found" in response.data  # Check if the error message appears

def test_weather_page_empty_city(client):
    # Simulate submitting an empty city name
    response = client.post('/', data={'city': ''})
    assert response.status_code == 200
    assert b"Enter city name" not in response.data  # Verify no error related to empty input