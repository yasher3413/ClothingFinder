# main.py

from recommendation import recommend_outfit

def display_outfit(outfit):
    print("\nRecommended Outfit:\n")
    for part, item in outfit.items():
        print(f"{part}:")
        print(f"  Brand: {item['brand']}")
        print(f"  Type: {item['type']}")
        print(f"  Material: {item['material']}")
        print(f"  Color: {item['color']}\n")

if __name__ == '__main__':
    city = input("Enter your city: ")
    outfit = recommend_outfit(city)
    if outfit:
        display_outfit(outfit)
    else:
        print("No suitable outfit found or error fetching weather data.")

