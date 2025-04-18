# app.py

from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify
)
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from flask_sqlalchemy import SQLAlchemy
from models import db, User, WardrobeItem, UserPreference, OutfitHistory, OutfitItem, WeatherCache
from recommendation import recommend_outfit
from wardrobe import (
    add_clothing_item, load_user_wardrobe, save_user_wardrobe
)
from weather import get_current_weather, parse_weather, API_KEY
from fashion_rules import (
    Occasion, OCCASION_REQUIREMENTS, get_style_level,
    get_pattern_type, score_outfit
)
from user_preferences import UserPreferences
import requests
import time
from forms import LoginForm, RegisterForm
import os
from config import config
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(config['development'])
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dresssense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        # Drop all tables first to ensure a clean slate
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

@app.cli.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    print('Initialized the database.')

# Initialize database tables
with app.app_context():
    try:
        # Check if tables exist by querying the User model
        User.query.first()
    except Exception as e:
        print("Tables don't exist, creating them...")
        db.create_all()
        print("Database tables created successfully!")

# List of city IDs for major cities
major_cities_ids = [
    5128581,  # New York
    2643743,  # London
    2988507,  # Paris
    1850147,  # Tokyo
    2147714,  # Sydney
    524901,   # Moscow
    292223,   # Dubai
    1880252,  # Singapore
    2950159,  # Berlin
    6167865   # Toronto
]

# Global variables for caching
cached_weather_data = None
last_update_time = 0

def get_major_cities_weather():
    global cached_weather_data, last_update_time
    current_time = time.time()
    # Update every 600 seconds (10 minutes)
    if not cached_weather_data or (current_time - last_update_time) > 600:
        city_ids = ','.join(map(str, major_cities_ids))
        url = (
            f"http://api.openweathermap.org/data/2.5/group?id={city_ids}"
            f"&appid={API_KEY}&units=metric"
        )
        response = requests.get(url)
        data = response.json()
        weather_data = []
        if 'list' in data:
            for city_data in data['list']:
                weather = parse_weather(city_data)
                if weather:
                    weather_data.append(weather)
            cached_weather_data = weather_data
            last_update_time = current_time
        else:
            print("Error fetching group weather data:", data)
            cached_weather_data = []
    return cached_weather_data

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            if existing_user.username == username:
                flash('Username already exists.')
            else:
                flash('Email already exists.')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        # Create a wardrobe for the new user
        save_user_wardrobe(username, [])
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    outfit = None
    weather = None
    error = None
    occasion_rules = None
    outfit_scores = None
    major_cities_weather = get_major_cities_weather()
    occasions = [occasion.name.lower() for occasion in Occasion]

    if request.method == 'POST':
        try:
            city = request.form['city']
            occasion_name = request.form.get('occasion')
            
            # Debug logging
            print(f"Processing request for city: {city}, occasion: {occasion_name}")
            
            occasion = None
            if occasion_name:
                try:
                    occasion = Occasion[occasion_name.upper()]
                except KeyError:
                    error = f"Invalid occasion: {occasion_name}"
                    print(f"Error: {error}")
                    return render_template(
                        'home.html',
                        outfit=outfit,
                        weather=weather,
                        error=error,
                        occasion_rules=occasion_rules,
                        outfit_scores=outfit_scores,
                        major_cities_weather=major_cities_weather,
                        occasions=occasions
                    )
            
            # Get weather data
            raw_weather = get_current_weather(city)
            print(f"Weather API response: {raw_weather}")
            
            if 'cod' in raw_weather and raw_weather['cod'] != 200:
                error = f"Weather API error: {raw_weather.get('message', 'Unknown error')}"
                print(f"Error: {error}")
                return render_template(
                    'home.html',
                    outfit=outfit,
                    weather=weather,
                    error=error,
                    occasion_rules=occasion_rules,
                    outfit_scores=outfit_scores,
                    major_cities_weather=major_cities_weather,
                    occasions=occasions
                )
            
            weather = parse_weather(raw_weather)
            if not weather:
                error = "Failed to parse weather data"
                print(f"Error: {error}")
                return render_template(
                    'home.html',
                    outfit=outfit,
                    weather=weather,
                    error=error,
                    occasion_rules=occasion_rules,
                    outfit_scores=outfit_scores,
                    major_cities_weather=major_cities_weather,
                    occasions=occasions
                )
            
            # Get outfit recommendation
            outfit_weather = recommend_outfit(city, current_user.username, occasion)
            if outfit_weather == (None, None):
                error = "Error fetching weather data. Please check the city name and try again."
            else:
                outfit, weather = outfit_weather
                if not outfit:
                    error = "No suitable outfit found for your wardrobe."
                else:
                    # Get occasion rules if an occasion was specified
                    if occasion:
                        occasion_rules = OCCASION_REQUIREMENTS[occasion]
                    
                    # Calculate outfit scores
                    color_score, style_score, pattern_score, preference_score = score_outfit(
                        outfit, occasion
                    )
                    total_score = (
                        color_score * 0.3 +
                        style_score * 0.25 +
                        pattern_score * 0.2 +
                        preference_score * 0.25
                    )
                    
                    outfit_scores = {
                        'color_score': color_score,
                        'style_score': style_score,
                        'pattern_score': pattern_score,
                        'preference_score': preference_score,
                        'total_score': total_score
                    }
                    
                    # Add style level and pattern information to each item
                    for item in outfit.values():
                        item['style_level'] = get_style_level(item['type']).value
                        pattern = get_pattern_type(item['type'], item['color'])
                        item['pattern_type'] = pattern.type.value
                        item['pattern_scale'] = pattern.scale
                        item['pattern_density'] = pattern.density
                        
                        # Add complete item details
                        wardrobe = load_user_wardrobe(current_user.username)
                        matching_item = next(
                            (i for i in wardrobe if i['id'] == item['id']),
                            None
                        )
                        if matching_item:
                            item.update(matching_item)
        except Exception as e:
            error = f"An error occurred: {str(e)}"
            print(f"Unexpected error: {str(e)}")
            import traceback
            print(traceback.format_exc())
    
    return render_template(
        'home.html',
        outfit=outfit,
        weather=weather,
        error=error,
        occasion_rules=occasion_rules,
        outfit_scores=outfit_scores,
        major_cities_weather=major_cities_weather,
        occasions=occasions
    )

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    message = None
    if request.method == 'POST':
        # Get item details from the form
        item = {
            "id": None,  # Will be assigned automatically
            "brand": request.form['brand'],
            "type": request.form['type'],
            "material": request.form['material'],
            "color": request.form['color'],
            "warmth_level": int(request.form['warmth_level']),
            "category": request.form['category'],
            "image_url": request.form['image_url']
        }
        # Add the item to the user's wardrobe
        add_clothing_item(item, current_user.username)
        message = "Item added successfully!"
    return render_template('add_item.html', message=message)

@app.route('/wardrobe')
@login_required
def wardrobe():
    try:
        wardrobe_items = load_user_wardrobe(current_user.username)
        # Check if the request wants JSON
        if request.headers.get('Accept') == 'application/json':
            # Ensure each item has a category field
            for item in wardrobe_items:
                if 'category' not in item:
                    # Infer category from type if not present
                    item_type = item.get('type', '').lower()
                    if 'shirt' in item_type or 'top' in item_type or 'blouse' in item_type:
                        item['category'] = 'tops'
                    elif 'pant' in item_type or 'skirt' in item_type or 'short' in item_type:
                        item['category'] = 'bottoms'
                    elif 'jacket' in item_type or 'coat' in item_type or 'sweater' in item_type:
                        item['category'] = 'outerwear'
                    elif 'shoe' in item_type or 'boot' in item_type or 'sneaker' in item_type:
                        item['category'] = 'shoes'
                    elif 'accessory' in item_type or 'jewelry' in item_type or 'bag' in item_type:
                        item['category'] = 'accessories'
                    else:
                        item['category'] = 'other'
            return jsonify(wardrobe_items)
        return render_template('wardrobe.html', wardrobe=wardrobe_items)
    except Exception as e:
        print(f"Error loading wardrobe: {str(e)}")
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'error': 'Failed to load wardrobe items'}), 500
        flash('Failed to load wardrobe items.')
        return render_template('wardrobe.html', wardrobe=[])

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    wardrobe = load_user_wardrobe(current_user.username)
    item = next(
        (i for i in wardrobe if i['id'] == item_id),
        None
    )
    if not item:
        flash('Item not found.')
        return redirect(url_for('wardrobe'))
    if request.method == 'POST':
        # Update item details
        item['brand'] = request.form['brand']
        item['type'] = request.form['type']
        item['material'] = request.form['material']
        item['color'] = request.form['color']
        item['warmth_level'] = int(request.form['warmth_level'])
        item['category'] = request.form['category']
        item['image_url'] = request.form['image_url']
        save_user_wardrobe(current_user.username, wardrobe)
        flash('Item updated successfully.')
        return redirect(url_for('wardrobe'))
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    wardrobe = load_user_wardrobe(current_user.username)
    item = next(
        (i for i in wardrobe if i['id'] == item_id),
        None
    )
    if not item:
        flash('Item not found.')
    else:
        wardrobe.remove(item)
        save_user_wardrobe(current_user.username, wardrobe)
        flash('Item deleted.')
    return redirect(url_for('wardrobe'))

@app.route('/preferences')
@login_required
def preferences():
    user_preferences = UserPreferences(current_user.username)
    return render_template('preferences.html', preferences=user_preferences.preferences)

@app.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    user_preferences = UserPreferences(current_user.username)
    new_preferences = {
        "favorite_colors": request.form.getlist('favorite_colors'),
        "favorite_styles": request.form.getlist('favorite_styles'),
        "favorite_patterns": request.form.getlist('favorite_patterns'),
        "disliked_colors": request.form.getlist('disliked_colors'),
        "disliked_styles": request.form.getlist('disliked_styles'),
        "disliked_patterns": request.form.getlist('disliked_patterns')
    }
    user_preferences.update_preferences(new_preferences)
    flash('Preferences updated successfully!')
    return redirect(url_for('preferences'))

@app.route('/outfits')
@login_required
def outfits():
    # Get user's outfit history
    outfit_history = OutfitHistory.query.filter_by(user_id=current_user.id).order_by(OutfitHistory.created_at.desc()).all()
    
    # Format the outfit data for the template
    formatted_outfits = []
    for outfit in outfit_history:
        outfit_data = {
            'id': outfit.id,
            'occasion': outfit.occasion,
            'weather_condition': outfit.weather_condition,
            'created_at': outfit.created_at,
            'rating': 5,  # Default rating
            'items': []
        }
        
        # Get items for this outfit
        for item in outfit.items:
            wardrobe_item = {
                'id': item.item_id,
                'type': item.type,
                'color': item.color
            }
            outfit_data['items'].append({'item': wardrobe_item})
        
        formatted_outfits.append(outfit_data)
    
    return render_template('outfits.html', outfit_history=formatted_outfits)

@app.route('/profile')
@login_required
def profile():
    # Get user's profile information
    user = current_user
    wardrobe_count = WardrobeItem.query.filter_by(user_id=user.id).count()
    outfit_count = OutfitHistory.query.filter_by(user_id=user.id).count()
    return render_template('profile.html', 
                         user=user, 
                         wardrobe_count=wardrobe_count,
                         outfit_count=outfit_count)

@app.route('/settings')
@login_required
def settings():
    # Get user's settings and preferences
    user = current_user
    preferences = UserPreference.query.filter_by(user_id=user.id).first()
    return render_template('settings.html', user=user, preferences=preferences)

@app.route('/outfits/create', methods=['POST'])
@login_required
def create_outfit():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['occasion', 'weather', 'items']):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
            
        if not data['items']:
            return jsonify({'success': False, 'message': 'No items selected'}), 400

        # Create new outfit history entry
        outfit = OutfitHistory(
            user_id=current_user.id,
            occasion=data['occasion'],
            weather_condition=data['weather'],
            created_at=datetime.utcnow()
        )
        db.session.add(outfit)
        db.session.flush()  # Get the outfit ID

        # Add outfit items
        wardrobe = load_user_wardrobe(current_user.username)
        wardrobe_dict = {item['id']: item for item in wardrobe}
        
        for item_id in data['items']:
            # Find the item in the wardrobe
            wardrobe_item = wardrobe_dict.get(item_id)
            if wardrobe_item:
                outfit_item = OutfitItem(
                    outfit_id=outfit.id,
                    item_id=item_id,
                    type=wardrobe_item['type'],
                    color=wardrobe_item['color']
                )
                db.session.add(outfit_item)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Outfit created successfully'})

    except Exception as e:
        db.session.rollback()
        print(f"Error creating outfit: {str(e)}")
        return jsonify({'success': False, 'message': f'Failed to create outfit: {str(e)}'}), 500

@app.route('/initialize_wardrobe')
@login_required
def initialize_wardrobe():
    try:
        # Sample wardrobe items
        sample_items = [
            {
                "id": 1,
                "type": "T-Shirt",
                "brand": "Nike",
                "color": "Blue",
                "material": "Cotton",
                "category": "tops",
                "warmth_level": 2,
                "image_url": "/static/images/placeholder.png"
            },
            {
                "id": 2,
                "type": "Jeans",
                "brand": "Levi's",
                "color": "Dark Blue",
                "material": "Denim",
                "category": "bottoms",
                "warmth_level": 3,
                "image_url": "/static/images/placeholder.png"
            },
            {
                "id": 3,
                "type": "Jacket",
                "brand": "The North Face",
                "color": "Black",
                "material": "Polyester",
                "category": "outerwear",
                "warmth_level": 4,
                "image_url": "/static/images/placeholder.png"
            },
            {
                "id": 4,
                "type": "Sneakers",
                "brand": "Adidas",
                "color": "White",
                "material": "Canvas",
                "category": "shoes",
                "warmth_level": 2,
                "image_url": "/static/images/placeholder.png"
            },
            {
                "id": 5,
                "type": "Watch",
                "brand": "Casio",
                "color": "Silver",
                "material": "Metal",
                "category": "accessories",
                "warmth_level": 1,
                "image_url": "/static/images/placeholder.png"
            }
        ]
        
        # Save the sample items to the user's wardrobe
        save_user_wardrobe(current_user.username, sample_items)
        
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': True, 'message': 'Wardrobe initialized with sample items'})
        
        flash('Wardrobe initialized with sample items!')
        return redirect(url_for('wardrobe'))
        
    except Exception as e:
        print(f"Error initializing wardrobe: {str(e)}")
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'error': 'Failed to initialize wardrobe'}), 500
        flash('Failed to initialize wardrobe.')
        return redirect(url_for('wardrobe'))

if __name__ == '__main__':
    app.run(debug=True)
