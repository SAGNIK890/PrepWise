
from fastapi import APIRouter
from prepwise2 import db

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/")
def list_recipes():
    recipes = list(db.recipes.find())
    for r in recipes:
        r["_id"] = str(r["_id"])
    return recipes
