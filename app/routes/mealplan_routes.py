# app/routes/mealplan_routes.py
from fastapi import APIRouter, HTTPException
from prepwise2 import db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/mealplans", tags=["Meal Plans"])

@router.get("/{user_id}")
def get_user_mealplans(user_id: str):
    plans = list(db.meal_plans.find({"user_id": user_id}))
    for p in plans:
        p["_id"] = str(p["_id"])
    return plans

@router.post("/")
def create_meal_plan(data: dict):
    data["created_at"] = datetime.utcnow()
    res = db.meal_plans.insert_one(data)
    return {"meal_plan_id": str(res.inserted_id)}
