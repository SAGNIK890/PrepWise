# app/routes/agent_routes.py
from fastapi import APIRouter, HTTPException
from prepwise2 import db
from bson import ObjectId
from datetime import datetime
import random
import uuid

router = APIRouter(prefix="/agent", tags=["Agentic AI"])

@router.post("/generate/{user_id}")
def generate_weekly_plan(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(404, "User not found")

    recipes = list(db.recipes.find())
    if not recipes:
        raise HTTPException(404, "No recipes found")

    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    week_plan = {}
    for d in days:
        chosen = random.sample(recipes, k=min(3, len(recipes)))
        week_plan[d] = {
            "breakfast": str(chosen[0]["_id"]),
            "lunch": str(chosen[1]["_id"]) if len(chosen) > 1 else str(chosen[0]["_id"]),
            "dinner": str(chosen[2]["_id"]) if len(chosen) > 2 else str(chosen[0]["_id"])
        }

    plan_doc = {
        "user_id": str(user["_id"]),
        "week_start": datetime.utcnow().strftime("%Y-%m-%d"),
        "days": week_plan,
        "created_at": datetime.utcnow(),
    }
    db.meal_plans.insert_one(plan_doc)

    agent_doc = {
        "name": "PlanAgent_v1",
        "run_id": str(uuid.uuid4()),
        "input_params": {"diet": user.get("preferences", {}).get("diet", "omnivore")},
        "decision_summary": "Auto-generated weekly plan using random sampling heuristic.",
        "created_at": datetime.utcnow(),
    }
    db.agents.insert_one(agent_doc)

    return {"status": "success", "message": "Weekly plan and agent log created"}
