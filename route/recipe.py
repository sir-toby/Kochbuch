from flask import request, Blueprint
from service.recipe import *

recipeApi = Blueprint('recipe', __name__)


@recipeApi.route("/recipes/", methods=["GET"])
def get_recipes():
    return getAllRecipesFromDatabase()


@recipeApi.route("/recipes/<recipeId>", methods=["GET"])
def get_recipe_id(recipeId):
    return getRecipeFromDatabaseById(recipeId)


@recipeApi.route("/recipes/<recipeName>", methods=["GET"])
def get_recipe_name(recipeName):
    return getRecipeFromDatabaseByName(recipeName)


@recipeApi.route("/recipes/", methods=["POST"])
def add_recipe():
    try:
        addRecipeToDatabase(request.json)
    except ValueError:
        return "Recipe already exists", 409
    else:
        return "Successfully added", 200
