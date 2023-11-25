import pytest
from pytest_mock import mocker

import test.test_constants

import api.service.ingredient
from api.schema.ingredient import IngredientSchema


ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)

class TestGetIngredientById(): 
    def test_get_ingredient_by_id_successful(self, mocker):
        mocker.patch('api.service.ingredient.IngredientModel.getById', return_value=test.test_constants.testIngredientModel)
        assert api.service.ingredient.getIngredientById(1) == ingredient_schema.dump(test.test_constants.testIngredientModel)
    
    def test_get_ingredient_by_id_not_found(self, mocker): 
        with pytest.raises(NameError):
            mocker.patch('api.service.ingredient.IngredientModel.getById', side_effect = NameError)
            api.service.ingredient.getIngredientById(1)
    
    def test_get_ingredient_by_id_error(self, mocker): 
        with pytest.raises(Exception): 
            mocker.patch('api.service.ingredient.IngredientModel.getById', side_effect=Exception)
            api.service.ingredient.getIngredientById(1)


class TestGetAllIngredients(): 
    def test_get_all_ingredients_successful(self, mocker): 
        mocker.patch('api.service.ingredient.IngredientModel.getAll', return_value=test.test_constants.testAllIngredients)
        assert api.service.ingredient.getAllIngredients() == ingredients_schema.dump(test.test_constants.testAllIngredients)
    
    def test_get_all_ingredients_empty(self, mocker): 
        mocker.patch('api.service.ingredient.IngredientModel.getAll', return_value=[])
        assert api.service.ingredient.getAllIngredients() == ingredients_schema.dump([])
    
    def test_get_all_ingredients_error(self): 
        with pytest.raises(Exception): 
            mocker.patch('api.service.ingredient.IngredientModel.getAll', side_effect=Exception)
            api.service.ingredient.getAllIngredients()

class TestAddIngredient(): 
    def test_add_ingredient_successful(self, mocker): 
        mocker.patch('api.service.ingredient.IngredientModel.add', return_value=test.test_constants.testIngredientModel2)
        assert api.service.ingredient.addIngredient(test.test_constants.testJsonIngredient2) == ingredient_schema.dump(test.test_constants.testIngredientModel2)
    
    def test_add_ingredient_already_exists(self, mocker): 
        mocker.patch('api.service.ingredient.IngredientModel.add', side_effect=ValueError("Ingredient already exists"))
        mocker.patch('api.service.ingredient.IngredientModel.getByName', return_value=test.test_constants.testIngredientModel2)
        assert api.service.ingredient.addIngredient(test.test_constants.testJsonIngredient2) == ingredient_schema.dump(test.test_constants.testIngredientModel2)

    def test_add_ingredient_error(self, mocker): 
        with pytest.raises(TypeError): 
            mocker.patch('api.service.ingredient.IngredientModel.add', side_effect=Exception)
            api.service.ingredient.addIngredient(test.test_constants.testJsonIngredient2)

    