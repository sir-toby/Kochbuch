from flask import request, Blueprint
from service.ingredient import *
from model.ingredient import IngredientModel

ingredientApi = Blueprint('ingredient', __name__)


@ingredientApi.route("/ingredients/", methods=["GET"])
def get_ingredients():
    try:
        allIngredients = getAllIngredients()
    except:
        return ValueError("Unknown technical error"), 500

    return allIngredients, 200


@ingredientApi.route("/ingredients/<ingredientId>", methods=["GET"])
def get_ingredient_id(ingredientId):
    try:
        ingredient = getIngredientById(ingredientId)
    except:
        return ValueError("Unknown technial error"), 500
    return ingredient, 200


"""
@ingredientApi.route("/ingredients/<ingredientName>", methods=["GET"])
def get_ingredient_name(ingredientName):
    try:
        ingredient = getIngredientByName(ingredientName)
    except:
        return ValueError("Unknown technical error"), 500
    return ingredient, 200
"""


@ingredientApi.route("/ingredients/", methods=["POST"])
def add_ingredients():
    try:
        ingredient = addIngredient(request.json)
    except:
        return ValueError("Unknown technical error"), 500
    return ingredient, 200
