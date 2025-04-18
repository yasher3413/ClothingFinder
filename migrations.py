from flask_migrate import Migrate
from app import app, db
from models import User, WardrobeItem, UserPreference, OutfitHistory, OutfitItem, WeatherCache

migrate = Migrate(app, db)

def init_db():
    """Initialize the database and create all tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_db() 