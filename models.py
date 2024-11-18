# models.py

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    items = db.relationship('Item', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    brand = db.Column(db.String(100))
    type = db.Column(db.String(100))
    material = db.Column(db.String(100))
    color = db.Column(db.String(50))
    style = db.Column(db.String(50))
    category = db.Column(db.String(50))
    warmth_level = db.Column(db.Integer)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<Item {self.brand} {self.type}>'
