from flask import request, Blueprint
from service.recipe import *

recipeApi = Blueprint('recipe', __name__)


@recipeApi.route("/recipes/", methods=["GET"])
def get_recipes():
    return getAllRecipesFromDatabases()


@recipeApi.route("/recipes/<recipeId>", methods=["GET"])
def get_recipe_id(recipeId):
    return getRecipeFromDatabaseById(recipeId)


@recipeApi.route("/recipes/<recipeName>", methods=["GET"])
def get_recipe_name(recipeName):
    return getRecipeFromDatabaseByName(recipeName)


@recipeApi.route("/recipes/", methods=["POST"])
def add_recipe():
    try:
        veggie = request.form["veggie"]
    except:
        veggie = False
    try:
        addRecipeToDatabase(RecipeModel(None, request.form["name"], veggie))
    except ValueError:
        return "Recipe already exists", 409
