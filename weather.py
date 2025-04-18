# weather.py

import requests

API_KEY = '24b6462c4875e9948fe95ea6e8133055'  

def get_current_weather(city):
    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&appid={API_KEY}&units=metric"
        )
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        print("API Response Data:", data)  # For debugging
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {str(e)}")
        return {'cod': 500, 'message': str(e)}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {'cod': 500, 'message': str(e)}

def parse_weather(data):
    try:
        if 'main' not in data:
            print(
                f"Error fetching weather data: "
                f"{data.get('message', 'Unknown error')}"
            )
            return None
        
        if 'cod' in data and data['cod'] != 200:
            print(f"Weather API error: {data.get('message', 'Unknown error')}")
            return None
            
        weather = {
            'city': data.get('name', 'Unknown'),
            'temperature': data['main'].get('temp'),
            'conditions': data['weather'][0].get('main'),
            'humidity': data['main'].get('humidity'),
            'wind_speed': data['wind'].get('speed')
        }
        return weather
    except Exception as e:
        print(f"Error parsing weather data: {str(e)}")
        return None
