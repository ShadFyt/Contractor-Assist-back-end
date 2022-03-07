from typing import Dict, List
import json
from fastapi.encoders import jsonable_encoder
from fastapi import status


def get_recipes_name(data) -> List:
    recipes = data[0].get("recipes")
    return [recipes[i].get("name") for i in range(len(recipes))]


def get_single_recipe(data, recipe_name: str) -> Dict:
    recipes = data[0].get("recipes")

    return next(
        (
            {
                "details": {
                    "ingredients": recipes[i]["ingredients"],
                    "numSteps": len(recipes[i]["instructions"]),
                }
            }
            for i in range(len(recipes))
            if recipes[i]["name"] == recipe_name
        ),
        {},
    )


def add_recipe(data, new_recipe):
    recipes = data[0].get("recipes")
    file = data[1]
    list_of_recipes = get_recipes_name(data)
    if new_recipe.name in list_of_recipes:
        return {status.HTTP_400_BAD_REQUEST: "Recipe already exists"}

    recipes.append(jsonable_encoder(new_recipe))
    file.seek(0)
    json.dump(data[0], file, indent=4)
    return new_recipe
