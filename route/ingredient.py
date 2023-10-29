from flask import request, Blueprint
from service.ingredient import *
from model.ingredient import IngredientModel

ingredientApi = Blueprint('ingredient', __name__)


@ingredientApi.route("/ingredients/", methods=["GET"])
def get_recipes():
    return getAllIngredientsFromDatabase()


@ingredientApi.route("/ingredients/<ingredientId>", methods=["GET"])
def get_recipe_id(ingredientId):
    return getIngredientFromDatabaseById(ingredientId)


@ingredientApi.route("/ingredients/<ingredientName>", methods=["GET"])
def get_recipe_name(ingredientName):
    return getIngredientFromDatabaseByName(ingredientName)


@ingredientApi.route("/ingredients/", methods=["POST"])
def addIngredients():
    ingredients = [IngredientModel(None, ingredient.name, ingredient.amount, ingredient.unit)
                   for ingredient in request.json]
    try:
        addIngredientsToDatabase(ingredients)
    except ValueError:
        return "Ingredient already exists", 409
