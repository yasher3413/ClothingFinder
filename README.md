# ClothingFinder

**ClothingFinder** is a Python web application that recommends outfits based on the current weather and your personal wardrobe. The app ensures that outfit recommendations vary each time you enter a city and that items in the outfit match based on attributes like color, style, and material.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x.x-orange.svg)](https://flask.palletsprojects.com/)

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User Authentication:**  
  Users can register, log in, and maintain separate wardrobes.

- **Wardrobe Management:**  
  Add, edit, and delete clothing items with attributes (e.g., brand, type, material, color, style, warmth level).

- **Weather Integration:**  
  Fetches current weather data using the [OpenWeatherMap API](https://openweathermap.org/api).

- **Outfit Recommendations:**  
  Generates varied and matching outfits based on weather conditions, item colors, styles, and materials.

- **Randomized Results:**  
  Introduces randomness so you get different recommendations even when entering the same city multiple times.

- **Animations & Transitions:**  
  Includes loading spinners, hover effects, and page transitions for a smooth user experience.

---

## Prerequisites

- **Python 3.7+**
- **pip:** (Python package manager)
- **Virtual environment:** (recommended)
- **[OpenWeatherMap API Key](https://openweathermap.org/api)**
- **SQLite:** (default database) or any other database supported by SQLAlchemy

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/ClothingFinder.git
   cd ClothingFinder

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
# On Windows:
    venv\Scripts\activate
# On macOS/Linux:
    source venv/bin/activate
3. **Install Dependencies**
    ```bash
   pip install -r requirements.txt
4. **Set Up the Database:**
By default, uses SQLite (clothingfinder.db).
Modify app.config['SQLALCHEMY_DATABASE_URI'] in app.py if you want a different database.

5. **Run Database Migrations (if using Flask-Migrate)**
     ```bash
   flask db upgrade

# Configuration
1. **Secret Key**
  For Development: In app.py, set:
    ```bash
    app.secret_key = 'your_secure_key'

  For Production: Use environment variables or secure storage:

    export SECRET_KEY='your_secure_key'

    import os
    app.secret_key = os.environ.get('SECRET_KEY', 'default_key')

2. **OpenWeatherMap API Key**
Replace 'your_api_key' in get_weather_data(city) with your actual API key.

3. **Environment Variables** (Recommended)
Use a .env file or system environment variables to keep your secrets out of version control.

# Usage
1. **Start the Flask Application:**
    ```bash
    python app.py
The application will run at http://127.0.0.1:5000/ by default.

2. **Register and Log In:**
Create an account or log in with existing credentials.

3. **Manage Your Wardrobe:**
Add items to your wardrobe with attributes like color, material, style, warmth level, etc.

4. **Get Outfit Recommendations:**
Enter a city name on the home page.
The app fetches the current weather and recommends a matching outfit from your wardrobe.
The outfit recommendation is randomized to provide fresh results each time.

5. **Edit or Delete Items:**
Go to My Wardrobe to edit or delete existing items.

# Contributing
1. **Fork the Repository**
2. **Create a Feature Branch**
    ```bash
    git checkout -b feature/new-feature
3. **Make Your Changes and commit **
    ```bash
   git commit -m "Add new feature"
4. **Push to Your Branch**
    ```bash
   git push origin feature/new-feature
5. **Open a Pull Request on the main repository**

# License
This project is licensed under the MIT License. Feel free to modify and distribute as per the terms of the license.
```bash
This **README.md** is formatted using Markdown and includes all necessary sections for a professional GitHub presentation. Adjust any specific paths, environment variables, or descriptions to match your actual application details.
