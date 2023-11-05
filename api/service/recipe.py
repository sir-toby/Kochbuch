from api.model.recipe import RecipeModel
from api.model.ingredientForRecipe import IngredientForRecipeModel
from api.model.ingredient import IngredientModel
from api.schema.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


def getRecipeByName(name):
    return recipe_schema.dump(RecipeModel.getByName(name))


def getRecipeById(recipeId):
    return recipe_schema.dump(RecipeModel.getById(recipeId))


def getAllRecipes():
    return recipes_schema.dump(RecipeModel.getAll())


def addRecipe(jsonRecipe):
    try:
        veggie = jsonRecipe["veggie"]
    except:
        veggie = False
    recipe = RecipeModel(None, jsonRecipe["name"], veggie,
                         [IngredientForRecipeModel(IngredientModel(None, ingredient["name"], ingredient["unit"]), ingredient["amount"])
                          for ingredient in jsonRecipe["ingredients"]])

    try:
        recipe.add()
    except:
        raise ValueError("Unknown error")
    return recipe_schema.dump(recipe)
