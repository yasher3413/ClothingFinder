# DressSense

**DressSense** is a Python web application that recommends outfits based on the current weather and your personal wardrobe. The app ensures that outfit recommendations vary each time you enter a city and that items in the outfit match based on attributes like color, style, and material.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x.x-orange.svg)](https://flask.palletsprojects.com/)

## Features

- **Weather-based Recommendations**: Get outfit suggestions based on current weather conditions
- **Wardrobe Management**: Add and manage your clothing items with detailed attributes
- **Smart Matching**: Outfits are generated based on color, style, and material compatibility
- **User Preferences**: Customize your style preferences for better recommendations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DressSense.git
cd DressSense
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

5. Initialize the database:
```bash
flask db upgrade
```

## Usage

1. Start the application:
```bash
flask run
```

2. Open your browser and navigate to `http://localhost:5000`

3. Register a new account or log in

4. Add items to your wardrobe with details like:
   - Category (top, bottom, outerwear, etc.)
   - Color
   - Style
   - Material
   - Weather conditions

5. Enter a city name to get weather-based outfit recommendations

## Project Structure

```
DressSense/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   └── utils/
│       ├── weather.py
│       └── recommendation.py
├── migrations/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
├── tests/
├── config.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for the web framework
- SQLAlchemy for the ORM
- OpenWeatherMap API for weather data
- Bootstrap for the frontend framework
