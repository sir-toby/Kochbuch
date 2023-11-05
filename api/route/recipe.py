from flask import request, Blueprint
from api.service.recipe import *

recipeApi = Blueprint('recipe', __name__)


@recipeApi.route("/recipes/", methods=["GET"])
def get_recipes():
    try:
        recipes = getAllRecipes()
    except:
        return "Unknown technical error", 500
    return recipes, 200


@recipeApi.route("/recipes/<recipeId>", methods=["GET"])
def get_recipe_id(recipeId):
    try:
        recipe = getRecipeById(recipeId)
    except:
        return "Unknown technical error", 500
    return recipe, 200


@recipeApi.route("/recipes/<recipeName>", methods=["GET"])
def get_recipe_name(recipeName):
    try:
        recipe = getRecipeByName(recipeName)
    except:
        return "Unknown technical error", 500
    return recipe, 200


@recipeApi.route("/recipes/", methods=["POST"])
def add_recipe():
    try:
        recipe = addRecipe(request.json)
    except:
        return "Unknown technical error", 500
    return recipe, 200
