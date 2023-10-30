from flask import request, Blueprint
from service.ingredient import *
from model.ingredient import IngredientModel

ingredientApi = Blueprint('ingredient', __name__)


@ingredientApi.route("/ingredients/", methods=["GET"])
def get_ingredients():
    return getAllIngredientsFromDatabase()


@ingredientApi.route("/ingredients/<ingredientId>", methods=["GET"])
def get_ingredient_id(ingredientId):
    return getIngredientFromDatabaseById(ingredientId)


@ingredientApi.route("/ingredients/<ingredientName>", methods=["GET"])
def get_ingredient_name(ingredientName):
    return getIngredientFromDatabaseByName(ingredientName)


@ingredientApi.route("/ingredients/", methods=["POST"])
def addIngredients():
    req = request.json
    ingredient = IngredientModel(None, req["name"], req["unit"])
    try:
        addIngredientToDatabase(ingredient)
    except ValueError:
        return "Ingredient already exists", 409
