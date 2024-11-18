# app.py

from flask import (
    Flask, render_template, request, redirect, url_for, flash
)
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from recommendation import recommend_outfit
from wardrobe import (
    add_clothing_item, load_user_wardrobe, save_user_wardrobe
)
from weather import get_current_weather, parse_weather, API_KEY
import requests
import time
from forms import LoginForm, RegisterForm
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory user store for simplicity
users = {}

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id  # id should be a string
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

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
        password = form.password.data
        # Check if username already exists
        for user in users.values():
            if user.username == username:
                flash('Username already exists.')
                return redirect(url_for('register'))
        user_id = str(len(users) + 1)
        new_user = User(user_id, username, password)
        users[user_id] = new_user
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
        for user in users.values():
            if user.username == username and user.password == password:
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
    major_cities_weather = get_major_cities_weather()

    if request.method == 'POST':
        city = request.form['city']
        try:
            outfit_weather = recommend_outfit(city, current_user.username)
            if outfit_weather == (None, None):
                error = (
                    "Error fetching weather data. "
                    "Please check the city name and try again."
                )
            else:
                outfit, weather = outfit_weather
                if not outfit:
                    error = (
                        "No suitable outfit found for your wardrobe."
                    )
        except Exception as e:
            error = f"An error occurred: {str(e)}"
    return render_template(
        'home.html',
        outfit=outfit,
        weather=weather,
        error=error,
        major_cities_weather=major_cities_weather
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
    wardrobe_items = load_user_wardrobe(current_user.username)
    return render_template('wardrobe.html', wardrobe=wardrobe_items)

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

if __name__ == '__main__':
    app.run(debug=True)
