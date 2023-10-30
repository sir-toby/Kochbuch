from model.ingredient import IngredientModel
from schema.ingredient import IngredientSchema

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


def getIngredientByName(name):
    return ingredient_schema.dump(IngredientModel.getByName(name))


def getIngredientById(ingredientId):
    return ingredient_schema.dump(IngredientModel.getById(ingredientId))


def getAllIngredients():
    return ingredients_schema.dump(IngredientModel.getAll())


def addIngredient(ingredientJson):
    ingredient = IngredientModel(None, ingredientJson["name"], ingredientJson["unit"])
    try:
        ingredient.add()
    except:
        raise ValueError("Unknown error")
    return ingredients_schema.dump(ingredient)
