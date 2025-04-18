import json
import os

class UserPreferences:
    def __init__(self, username):
        self.username = username
        self.preferences_file = f"user_data/{username}_preferences.json"
        self.preferences = self._load_preferences()

    def _load_preferences(self):
        """Load user preferences from file or return default preferences"""
        default_preferences = {
            "favorite_colors": [],
            "favorite_styles": [],
            "favorite_patterns": [],
            "disliked_colors": [],
            "disliked_styles": [],
            "disliked_patterns": []
        }

        if not os.path.exists(self.preferences_file):
            return default_preferences

        try:
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return default_preferences

    def update_preferences(self, new_preferences):
        """Update user preferences and save to file"""
        self.preferences = new_preferences
        os.makedirs(os.path.dirname(self.preferences_file), exist_ok=True)
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f) 