import pytest
from pytest_mock import mocker
import json
from app import create_app
import api.route.ingredient
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

class TestGetIngredients():

    def test_get_ingredients_empty_list(self, mocker):
        mocker.patch('api.route.ingredient.getAllIngredients', return_value=[])
        assert api.route.ingredient.get_ingredients() == ([], 200)

    def test_get_ingredients_exception(self, mocker):
        mocker.patch('api.route.ingredient.getAllIngredients', side_effect=Exception())
        assert api.route.ingredient.get_ingredients() == ("Unknown technical error", 500)

    def test_get_ingredients_valid(self, mocker):
        mocker.patch('api.route.ingredient.getAllIngredients', return_value=test.test_constants.testJsonIngredientList)
        assert api.route.ingredient.get_ingredients() == (test.test_constants.testJsonIngredientList, 200)

class TestGetIngredientId():
    def test_get_ingredient_id_successful(self, mocker):
        mocker.patch('api.route.ingredient.getIngredientById', return_value=test.test_constants.testIngredientModel)
        assert api.route.ingredient.get_ingredient_id(1) == (test.test_constants.testIngredientModel, 200)
    
    def test_get_ingredient_id_notFound(self, mocker): 
        mocker.patch('api.route.ingredient.getIngredientById', side_effect=NameError)
        assert api.route.ingredient.get_ingredient_id(1) == ("Ingredient not found", 404)
    
    def test_get_ingredient_id_error(self, mocker): 
        mocker.patch('api.route.ingredient.getIngredientById', side_effect=Exception)
        assert api.route.ingredient.get_ingredient_id(1) == ("Unknown technical error", 500)

    def test_get_ingredient_id_missing_argument(self): 
            with pytest.raises(TypeError):
                api.route.ingredient.get_ingredient_id()

class TestAddIngredients():
    def test_add_ingredients_successful(self, mocker, client):
        mocker.patch('api.route.ingredient.addIngredient', return_value=test.test_constants.testJsonIngredient)
        response = client.post("/ingredients/", json=json.dumps(test.test_constants.testJsonIngredient), content_type='application/json')
        assert response.json == test.test_constants.testJsonIngredient 
        assert response.status_code == 200
    
    def test_add_ingredients_empty(self, client):
        response = client.post("/ingredients/", json=json.dumps(None), content_type='application/json')
        assert response.json == None 
        assert response.status_code == 500
    
    def test_add_ingredients_conflict(self, mocker, client): 
        mocker.patch('api.route.ingredient.addIngredient', side_effect=ValueError)
        response = client.post("/ingredients/", json=json.dumps(test.test_constants.testJsonIngredient), content_type='application/json')
        assert response.status_code == 409 
        assert response.json == None
        assert response.text == "Ingredient already exists"
    
    def test_add_ingredients_error(self): 
        assert api.route.ingredient.add_ingredients() == ("Unknown technical error", 500)
