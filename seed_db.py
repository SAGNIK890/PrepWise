
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["prepwise"]

def seed():
    db.users.delete_many({})
    db.recipes.delete_many({})
    db.ingredients.delete_many({})
    db.meal_plans.delete_many({})
    db.agents.delete_many({})
    db.feedback.delete_many({})

    user_id = db.users.insert_one({
        "name": "Test User",
        "email": "testuser@prepwise.com",
        "password_hash": "demo123",
        "preferences": {"diet": "vegan", "budget_per_week": 500},
        "created_at": datetime.utcnow()
    }).inserted_id

    db.recipes.insert_many([
        {"title": "Lentil Curry", "ingredients": [], "instructions": "Boil and spice lentils.", "diet_tags": ["vegan"], "nutrition": {"calories": 300}, "cost_estimate": 50},
        {"title": "Oats Bowl", "ingredients": [], "instructions": "Mix oats with fruits.", "diet_tags": ["vegetarian"], "nutrition": {"calories": 250}, "cost_estimate": 30}
    ])

    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed()
