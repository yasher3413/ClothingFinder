# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    wardrobe_items = db.relationship('WardrobeItem', backref='owner', lazy=True)
    preferences = db.relationship('UserPreference', backref='user', lazy=True, uselist=False)
    outfit_history = db.relationship('OutfitHistory', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class WardrobeItem(db.Model):
    __tablename__ = 'wardrobe_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brand = db.Column(db.String(100))
    type = db.Column(db.String(50), nullable=False)
    material = db.Column(db.String(50))
    color = db.Column(db.String(50), nullable=False)
    warmth_level = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_worn = db.Column(db.DateTime)
    times_worn = db.Column(db.Integer, default=0)
    
    # Relationships
    outfit_items = db.relationship('OutfitItem', backref='item', lazy=True)

    def __repr__(self):
        return f'<Item {self.brand} {self.type}>'

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    favorite_colors = db.Column(db.JSON, default=list)
    favorite_styles = db.Column(db.JSON, default=list)
    favorite_patterns = db.Column(db.JSON, default=list)
    disliked_colors = db.Column(db.JSON, default=list)
    disliked_styles = db.Column(db.JSON, default=list)
    disliked_patterns = db.Column(db.JSON, default=list)
    temperature_preference = db.Column(db.Float, default=20.0)  # Preferred temperature in Celsius
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OutfitHistory(db.Model):
    __tablename__ = 'outfit_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    occasion = db.Column(db.String(50))
    weather_condition = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer)  # User rating for the outfit (1-5)
    
    # Relationships
    items = db.relationship('OutfitItem', backref='outfit', lazy=True)

class OutfitItem(db.Model):
    __tablename__ = 'outfit_items'
    
    id = db.Column(db.Integer, primary_key=True)
    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit_history.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('wardrobe_items.id'), nullable=False)
    position = db.Column(db.String(50))  # e.g., "top", "bottom", "outerwear"

class WeatherCache(db.Model):
    __tablename__ = 'weather_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    conditions = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.Index('idx_weather_city_updated', 'city', 'updated_at'),)
