import pytest
from pytest_mock import mocker
import json 
from app import create_app
import api.route.recipe
import test.test_constants

@pytest.fixture()
def testApp():
    testApp = create_app()
    testApp.config.update({
        "TESTING": True,
    })
    yield testApp

    # clean up / reset resources here

@pytest.fixture()
def client(testApp):
    return testApp.test_client()

class TestGetRecipes():

    def test_get_recipes_empty_list(self, mocker):
        mocker.patch('api.route.recipe.getAllRecipes', return_value=[])
        assert api.route.recipe.get_recipes() == ([], 200)

    def test_get_recipes_exception(self, mocker):
        mocker.patch('api.route.recipe.getAllRecipes', side_effect=Exception())
        assert api.route.recipe.get_recipes() == ("Unknown technical error", 500)

    def test_get_recipes_valid(self, mocker):
        mockedRecipeList = 'mockedRecipe'
        mocker.patch('api.route.recipe.getAllRecipes', return_value=mockedRecipeList)
        assert api.route.recipe.get_recipes() == (mockedRecipeList, 200)

class TestGetRecipeId():
    def test_get_recipe_id_successful(self, mocker):
        mockedRecipe = '{"id": "1", "name": "testName", "unit": "g"}'
        mocker.patch('api.route.recipe.getRecipeById', return_value=mockedRecipe)
        assert api.route.recipe.get_recipe_id(1) == (mockedRecipe, 200)
    
    def test_get_recipe_id_notFound(self, mocker): 
        mocker.patch('api.route.recipe.getRecipeById', side_effect=NameError)
        assert api.route.recipe.get_recipe_id(1) == ("Recipe not found", 404)
    
    def test_get_recipe_id_error(self, mocker): 
        mocker.patch('api.route.recipe.getRecipeById', side_effect=Exception)
        assert api.route.recipe.get_recipe_id(1) == ("Unknown technical error", 500)

    def test_get_recipe_id_missing_argument(self): 
            with pytest.raises(TypeError):
                api.route.recipe.get_recipe_id()

class TestAddRecipes():
    
    def test_add_recipe_successful(self, mocker, client):
        mocker.patch('api.route.recipe.addRecipe', return_value=test.test_constants.testJsonRecipe2)
        response = client.post("/recipes/", json = json.dumps(test.test_constants.testJsonRecipe2), content_type='application/json')
        assert response.json == test.test_constants.testJsonRecipe2
        assert response.status_code == 200
    
    def test_add_recipe_conflict(self, mocker, client): 
        mocker.patch('api.route.recipe.addRecipe', side_effect=ValueError("Recipe already exists"))
        response = client.post("/recipes/", json = json.dumps(test.test_constants.testJsonRecipe2), content_type='application/json')
        assert response.json == None
        assert response.status_code == 409
        assert response.text == "Recipe already exists"
    
    def test_add_ingredients_error(self): 
        assert api.route.recipe.add_recipe() == ("Unknown technical error", 500)
