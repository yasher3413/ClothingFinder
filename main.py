# main.py

from recommendation import recommend_outfit
from fashion_rules import Occasion, get_style_level, get_pattern_type, OCCASION_REQUIREMENTS

def display_outfit(outfit, weather, occasion=None):
    print("\nRecommended Outfit:\n")
    
    # Display weather information
    print(f"Weather: {weather['temperature']}°C, {weather['description']}")
    if occasion:
        print(f"Occasion: {occasion.value.upper()}")
        print("\nOccasion Requirements:")
        requirements = OCCASION_REQUIREMENTS[occasion]
        print(f"- Style Level: {requirements['min_style_level'].value} to {requirements['max_style_level'].value}")
        if requirements['pattern_restrictions']:
            print(f"- Pattern Restrictions: {', '.join(p.value for p in requirements['pattern_restrictions'])}")
        if requirements['color_restrictions']:
            print(f"- Color Restrictions: {', '.join(requirements['color_restrictions'])}")
    
    print("\nOutfit Details:")
    for part, item in outfit.items():
        print(f"\n{part}:")
        print(f"  Brand: {item['brand']}")
        print(f"  Type: {item['type']}")
        print(f"  Material: {item['material']}")
        print(f"  Color: {item['color']}")
        print(f"  Style Level: {get_style_level(item['type']).value}")
        pattern = get_pattern_type(item['type'], item['color'])
        print(f"  Pattern: {pattern.type.value} ({pattern.scale}, {pattern.density})")
    
    # Display scoring information
    from fashion_rules import score_outfit
    color_score, style_score, pattern_score, preference_score = score_outfit(outfit, occasion)
    print("\nOutfit Scoring:")
    print(f"Color Harmony: {color_score:.2f}")
    print(f"Style Compatibility: {style_score:.2f}")
    print(f"Pattern Matching: {pattern_score:.2f}")
    print(f"Personal Preference: {preference_score:.2f}")
    total_score = (color_score * 0.3 + style_score * 0.25 + pattern_score * 0.2 + preference_score * 0.25)
    print(f"Total Score: {total_score:.2f}")

if __name__ == '__main__':
    city = input("Enter your city: ")
    occasion_input = input("Enter occasion (work/casual/formal/sport/party/date/travel/beach) or press Enter for none: ")
    occasion = None
    if occasion_input:
        try:
            occasion = Occasion[occasion_input.upper()]
        except KeyError:
            print("Invalid occasion. Using default recommendations.")
    
    outfit, weather = recommend_outfit(city, "yashgandhi34", occasion)
    if outfit:
        display_outfit(outfit, weather, occasion)
    else:
        print("No suitable outfit found or error fetching weather data.")

