from api.model.ingredient import IngredientModel
from api.schema.ingredient import IngredientSchema

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


def getIngredientByName(name):
    return ingredient_schema.dump(IngredientModel.getByName(name))


def getIngredientById(ingredientId):
    try:
        return ingredient_schema.dump(IngredientModel.getById(ingredientId))
    except NameError:
        raise NameError("Entry not found")
    except: 
        raise Exception

def getAllIngredients():
    return ingredients_schema.dump(IngredientModel.getAll())


def addIngredient(ingredientJson):
    ingredient = IngredientModel(None, ingredientJson["name"], ingredientJson["unit"])
    try:
        ingredient.add()
    except ValueError:
        return ingredient_schema.dump(ingredient.getByName(ingredient.name))
    except:
        raise TypeError("Unknown error")
    return ingredient_schema.dump(ingredient)
