# recommendation.py

from weather import get_current_weather, parse_weather
from wardrobe import load_user_wardrobe

def determine_temperature_category(temp):
    if temp <= 5:
        return 'Cold'
    elif 5 < temp <= 15:
        return 'Cool'
    elif 15 < temp <= 25:
        return 'Warm'
    else:
        return 'Hot'

def recommend_outfit(city, username):
    # Fetch and parse weather data
    raw_weather = get_current_weather(city)
    weather = parse_weather(raw_weather)
    if weather is None:
        # Return None values to indicate failure
        return None, None
    temp_category = determine_temperature_category(
        weather['temperature']
    )
    print(
        f"Temperature: {weather['temperature']}°C, "
        f"Category: {temp_category}"
    )

    # Load user's wardrobe
    wardrobe = load_user_wardrobe(username)

    # Desired warmth levels
    desired_warmth = {
        'Cold': 9,
        'Cool': 6,
        'Warm': 3,
        'Hot': 1
    }

    desired_level = desired_warmth[temp_category]

    # Decide which categories to include based on temperature
    if temp_category == 'Cold':
        categories = [
            'Top', 'Bottom', 'Outerwear',
            'Footwear', 'Accessory'
        ]
    elif temp_category == 'Cool':
        categories = [
            'Top', 'Bottom', 'Outerwear',
            'Footwear', 'Accessory'
        ]
    elif temp_category == 'Warm':
        categories = [
            'Top', 'Bottom', 'Footwear', 'Accessory'
        ]
    else:  # Hot
        categories = [
            'Top', 'Bottom', 'Footwear', 'Accessory'
        ]

    # Group clothes by category and find the closest warmth level
    outfit = {}
    for category in categories:
        items_in_category = [
            item for item in wardrobe
            if item['category'] == category
        ]
        if not items_in_category:
            continue  # No items in this category
        # Find item with warmth level closest to desired_level
        best_item = min(
            items_in_category,
            key=lambda x: abs(
                x['warmth_level'] - desired_level
            )
        )
        outfit[category] = best_item

    return outfit, weather
