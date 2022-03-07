from typing import List
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from services.recipes_utils import get_recipes_name, get_single_recipe, add_recipe
from dependencies import get_data

router = APIRouter(prefix="/recipes", tags=["recipes"])


class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    instructions: List[str]


@router.get("/", status_code=status.HTTP_200_OK)
def read_all_recipes(*, data=Depends(get_data)):
    list_recipes = get_recipes_name(data)
    return {"recipeNames": list_recipes}


@router.get("/details/{recipe_name}", status_code=status.HTTP_200_OK)
def read_one_recipe(*, data=Depends(get_data), recipe_name: str):
    return get_single_recipe(data, recipe_name)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_recipe(*, data=Depends(get_data), new_recipe: Recipe):
    return add_recipe(data, new_recipe)
