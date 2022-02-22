from typing import Dict, List


def get_recipes_name(data: Dict) -> List:
    return [data["recipes"][i]["name"] for i in range(len(data["recipes"]))]


def get_single_recipe(data: Dict, recipe_name: str) -> Dict:
    for i in range(len(data["recipes"])):
        if data["recipes"][i]["name"] == recipe_name:
            print(recipe_name)
            return {
                "details": {
                    "ingredients": data["recipes"][i]["ingredients"],
                    "numSteps": len(data["recipes"][i]["instructions"]),
                }
            }
    return {}
