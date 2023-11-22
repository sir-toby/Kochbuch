import pytest
from pytest_mock import mocker
import api.service.recipe
from api.schema.recipe import RecipeSchema
import test.test_constants


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

class TestGetRecipeById(): 
    def test_get_recipe_by_id_successful(self, mocker):
        mocker.patch('api.service.recipe.RecipeModel.getById', return_value=test.test_constants.testRecipeModel)
        assert api.service.recipe.getRecipeById(1) == recipe_schema.dump(test.test_constants.testRecipeModel)
    
    def test_get_recipe_by_id_not_found(self, mocker): 
        with pytest.raises(NameError):
            mocker.patch('api.service.recipe.RecipeModel.getById', side_effect = NameError)
            api.service.recipe.getRecipeById(1)
    
    def test_get_recipe_by_id_error(self, mocker): 
        with pytest.raises(Exception): 
            mocker.patch('api.service.recipe.RecipeModel.getById', side_effect=Exception)
            api.service.recipe.getRecipeById(1)


class TestGetAllRecipes(): 
    def test_get_all_recipes_successful(self, mocker): 
        mocker.patch('api.service.recipe.RecipeModel.getAll', return_value=test.test_constants.testAllRecipes)
        assert api.service.recipe.getAllRecipes() == recipes_schema.dump(test.test_constants.testAllRecipes)
    
    def test_get_all_recipes_empty(self, mocker): 
        mocker.patch('api.service.recipe.RecipeModel.getAll', return_value=[])
        assert api.service.recipe.getAllRecipes() == recipes_schema.dump([])
    
    def test_get_all_recipes_error(self): 
        with pytest.raises(Exception): 
            mocker.patch('api.service.recipe.RecipeModel.getAll', side_effect=Exception)
            api.service.recipe.getAllRecipes()

class TestAddRecipe(): 
    def test_add_recipe_successful(self, mocker): 
        mocker.patch('api.service.recipe.RecipeModel.add', return_value=test.test_constants.testRecipeModel2)
        assert api.service.recipe.addRecipe(test.test_constants.testJsonRecipe2) == recipe_schema.dump(test.test_constants.testRecipeModel2)
    
    def test_add_recipe_already_exists(self, mocker): 
        with pytest.raises(Exception):
             mocker.patch('api.service.recipe.RecipeModel.add', side_effect=ValueError("Recipe already exists"))
             api.service.recipe.addRecipe(test.test_constants.testJsonRecipe2)
    
    def test_add_recipe_relation_already_exists(self, mocker): 
        with pytest.raises(Exception): 
            mocker.patch('api.service.recipe.RecipeModel.add', side_effect=ValueError("Relation already exists"))
            api.service.recipe.addRecipe(test.test_constants.testJsonRecipe2)
    
        
    def test_add_recipe_error(self, mocker): 
        with pytest.raises(Exception): 
            mocker.patch('api.service.recipe.RecipeModel.add', side_effect=SyntaxError("Unknown error"))
            api.service.recipe.addRecipe(test.test_constants.testJsonRecipe2)

    