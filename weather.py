# weather.py

import requests

API_KEY = '24b6462c4875e9948fe95ea6e8133055'  

def get_current_weather(city):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&appid={API_KEY}&units=metric"
    )
    response = requests.get(url)
    data = response.json()
    print("API Response Data:", data)  # For debugging
    return data

def parse_weather(data):
    if 'main' not in data:
        print(
            f"Error fetching weather data: "
            f"{data.get('message', 'Unknown error')}"
        )
        return None
    weather = {
        'city_name': data.get('name', 'Unknown'),
        'temperature': data['main'].get('temp'),
        'condition': data['weather'][0].get('main'),
        'humidity': data['main'].get('humidity'),
        'wind_speed': data['wind'].get('speed')
    }
    return weather
