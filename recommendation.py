# recommendation.py

from weather import get_current_weather, parse_weather
from wardrobe import load_user_wardrobe
from fashion_rules import (
    score_outfit, UserPreferences, Occasion, StyleLevel,
    get_style_level, get_pattern_type
)
import random
from typing import Optional, Dict, List, Tuple

def determine_temperature_category(temp):
    if temp <= 5:
        return 'Cold'
    elif 5 < temp <= 15:
        return 'Cool'
    elif 15 < temp <= 25:
        return 'Warm'
    else:
        return 'Hot'

def generate_candidate_outfits(
    wardrobe: List[Dict],
    categories: List[str],
    desired_level: int,
    occasion: Optional[Occasion] = None,
    user_preferences: Optional[UserPreferences] = None,
    num_candidates: int = 20
) -> List[Dict]:
    """Generate multiple candidate outfits based on temperature and occasion requirements."""
    candidates = []
    
    for _ in range(num_candidates):
        outfit = {}
        for category in categories:
            items_in_category = [
                item for item in wardrobe
                if item['category'] == category
            ]
            if not items_in_category:
                continue
            
            # Filter items by warmth level (within 2 levels of desired)
            suitable_items = [
                item for item in items_in_category
                if abs(item['warmth_level'] - desired_level) <= 2
            ]
            
            if suitable_items:
                # If we have user preferences, prioritize favorite items
                if user_preferences:
                    favorite_items = [
                        item for item in suitable_items
                        if item['color'] in user_preferences.preferences["favorite_colors"] or
                        get_style_level(item['type']) in user_preferences.preferences["favorite_styles"]
                    ]
                    if favorite_items:
                        outfit[category] = random.choice(favorite_items)
                        continue
                
                outfit[category] = random.choice(suitable_items)
        
        if outfit:  # Only add if we have at least one item
            candidates.append(outfit)
    
    return candidates

def recommend_outfit(
    city: str,
    username: str,
    occasion: Optional[Occasion] = None
) -> Tuple[Optional[Dict], Optional[Dict]]:
    """Recommend an outfit based on weather, occasion, and user preferences."""
    # Fetch and parse weather data
    raw_weather = get_current_weather(city)
    weather = parse_weather(raw_weather)
    if weather is None:
        return None, None
    
    temp_category = determine_temperature_category(weather['temperature'])
    print(f"Temperature: {weather['temperature']}°C, Category: {temp_category}")

    # Load user's wardrobe and preferences
    wardrobe = load_user_wardrobe(username)
    user_preferences = UserPreferences(username)

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
        categories = ['Top', 'Bottom', 'Outerwear', 'Footwear', 'Accessory']
    elif temp_category == 'Cool':
        categories = ['Top', 'Bottom', 'Outerwear', 'Footwear', 'Accessory']
    elif temp_category == 'Warm':
        categories = ['Top', 'Bottom', 'Footwear', 'Accessory']
    else:  # Hot
        categories = ['Top', 'Bottom', 'Footwear', 'Accessory']

    # Generate multiple candidate outfits
    candidates = generate_candidate_outfits(
        wardrobe, categories, desired_level,
        occasion, user_preferences
    )
    
    if not candidates:
        return None, weather

    # Score each candidate outfit
    scored_outfits = []
    for outfit in candidates:
        color_score, style_score, pattern_score, preference_score = score_outfit(
            outfit, occasion, user_preferences
        )
        
        # Weighted scoring system
        total_score = (
            color_score * 0.3 +
            style_score * 0.25 +
            pattern_score * 0.2 +
            preference_score * 0.25
        )
        
        scored_outfits.append((outfit, total_score))

    # Sort by total score and return the best outfit
    scored_outfits.sort(key=lambda x: x[1], reverse=True)
    best_outfit = scored_outfits[0][0]
    
    # Store the recommended outfit in user preferences
    user_preferences.add_favorite_outfit(best_outfit, scored_outfits[0][1])
    
    return best_outfit, weather
