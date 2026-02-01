import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from auth import get_password_hash

load_dotenv()  # Load environment variables

# Correct way to get Mongo URI and DB name
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "Prepwise")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable not set!")

def seed():
    client = MongoClient(MONGO_URI)  # Only here, not at top-level
    db = client[DB_NAME]

    # Clear old data
    db.users.delete_many({})
    db.recipes.delete_many({})
    db.ingredients.delete_many({})
    db.meal_plans.delete_many({})
    db.agents.delete_many({})
    db.feedback.delete_many({})

    # Insert test user
    db.users.insert_one({
        "name": "Test User",
        "email": "testuser@prepwise.com",
        "password_hash": get_password_hash("demo123"),
        "preferences": {"diet": "vegan", "budget_per_week": 500},
        "created_at": datetime.utcnow()
    })

    # Insert some recipes
    db.recipes.insert_many([
        {"title": "Lentil Curry", "ingredients": [], "instructions": "Boil and spice lentils.", "diet_tags": ["vegan"], "nutrition": {"calories": 300}, "cost_estimate": 50},
        {"title": "Oats Bowl", "ingredients": [], "instructions": "Mix oats with fruits.", "diet_tags": ["vegetarian"], "nutrition": {"calories": 250}, "cost_estimate": 30}
    ])

    print("✅ Database seeded successfully!")

# Only run seed when called directly
if __name__ == "__main__":
    seed()
