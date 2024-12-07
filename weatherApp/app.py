from flask import Flask, render_template, request  # Import necessary modules from Flask
import requests  # Import requests to make HTTP calls to the weather API
import calendar
from datetime import datetime
from dotenv import load_dotenv
import os
import sys
load_dotenv()

# Ensure the project root is in PYTHONPATH for consistent imports
project_root = os.getenv("PYTHONPATH", os.path.abspath(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

app = Flask(__name__)  # Create a Flask application instance

API_KEY = os.getenv("API_KEY") # Store your OpenWeatherMap API key
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"  # URL for the weather API endpoint

@app.route('/', methods=['GET', 'POST'])  # Define the route for the index page
def index():
    weather_data = None  # Initialize weather_data variable to hold weather information
    if request.method == 'POST':  # Check if the request method is POST (form submission)
        city = request.form.get('city')  # Get the city name from the submitted form
        if city:  # Check if a city name was provided
            # Set up the parameters for the API request
            params = {
                'q': city,  # The city name
                'appid': API_KEY,  # Your API key for authentication
                'units': 'metric'  # Use 'metric' for Celsius or 'imperial' for Fahrenheit
            }
            response = requests.get(WEATHER_URL, params=params)  # Make a GET request to the weather API
            if response.status_code == 200:  # Check if the request was successful (HTTP 200)
                weather_data = response.json()  # Parse the JSON response
            else:
                weather_data = {"error": "City not found"}  # Handle the case where the city is not found
    # Render the index.html template, passing the weather data (if any) to it
    return render_template('index.html', weather=weather_data)

@app.route('/calendar')
def calendar_view():
    today = datetime.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    # Get the days in the month as a structured list
    cal = calendar.Calendar(firstweekday=0)  # 0 is Monday
    days_in_month = cal.monthdayscalendar(current_year, current_month)  # Get the month days in a structured format

    # Flatten the list
    flat_days = [day for week in days_in_month for day in week]  # Flatten the 2D list

    # Pass current month and day info
    return render_template(
        'calendar.html',
        days_in_month=flat_days,
        current_day=current_day,
        current_month=current_month,
        current_year=current_year,
        month_name=today.strftime('%B')  # Full month name
    )


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode for development
