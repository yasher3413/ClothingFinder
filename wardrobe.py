# wardrobe.py

import json
import os

def load_user_wardrobe(username):
    filename = f'wardrobe_{username}.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            wardrobe = json.load(file)
    else:
        wardrobe = []
    return wardrobe

def save_user_wardrobe(username, wardrobe):
    filename = f'wardrobe_{username}.json'
    with open(filename, 'w') as file:
        json.dump(wardrobe, file, indent=4)

def add_clothing_item(item, username):
    wardrobe = load_user_wardrobe(username)
    # Assign a new ID
    if wardrobe:
        max_id = max(
            existing_item['id'] for existing_item in wardrobe
            if existing_item['id'] is not None
        )
    else:
        max_id = 0
    item['id'] = max_id + 1
    wardrobe.append(item)
    save_user_wardrobe(username, wardrobe)
