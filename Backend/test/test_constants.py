from api.model.ingredient import IngredientModel
from api.model.ingredientForRecipe import IngredientForRecipeModel
from api.model.recipe import RecipeModel

testJsonIngredientString = '{"id": "1", "name": "testIngredient", "unit": "g"}'
testJsonIngredientList = '[{"id": "1", "name": "test2", "unit": "g"}, {"id": "99", "name": "testIngredient", "unit": "Stk"}]'

testJsonIngredient = {"id": "1", "name": "testIngredient", "unit": "g"}
testJsonIngredient2 = {"id": None, "name": "test2", "unit": "pcs"}

testIngredientModel = IngredientModel(1, "testIngredient", "g")
testIngredientModel2 = IngredientModel(None, "test2", "pcs")
testIngredientModel3 = IngredientModel(None, "test3", "mL")

testAllIngredients = [testIngredientModel, testIngredientModel2]

testIngredientForRecipeModel = IngredientForRecipeModel(testIngredientModel, 5)
testIngredientForRecipeModel2 = IngredientForRecipeModel(testIngredientModel2, 199)
testIngredientForRecipeModel3 = IngredientForRecipeModel(testIngredientModel3, 5)

testRecipeModel = RecipeModel(1, "Test", False, [testIngredientForRecipeModel, testIngredientForRecipeModel2])
testRecipeModel2 = RecipeModel(None, "Test2", False, [testIngredientForRecipeModel2, testIngredientForRecipeModel3])
testRecipeModel3 = RecipeModel(None, "awefhifdlfk", False, [testIngredientForRecipeModel2, testIngredientForRecipeModel3])

testJsonRecipe2 = {"id": "1", "name": "Test2", "veggie": "False", "ingredients": [{"id": None, "name": "test2", "unit": "pcs", "amount": 199}, {"id": None, "name": "test3", "unit": "mL", "amount": 5}]}

testAllRecipes = [testRecipeModel, testRecipeModel2]