import pytest
from pytest_mock import mocker
from unittest.mock import MagicMock
import sqlite3
from copy import deepcopy as copy

from infrastructure.db_setup import create_database
from infrastructure.createTestData import createTestData

import test.test_constants 

from api.model.recipe import RecipeModel
from api.model.ingredientForRecipe import IngredientForRecipeModel
from api.model.ingredient import IngredientModel


@pytest.fixture()
def conn():
    databaseName = ':memory:'
    conn = sqlite3.connect(databaseName, check_same_thread=False)
    yield conn
    conn.close()

@pytest.fixture()
def setup_db(conn):
    create_database(conn)
    createTestData(conn)

def dbMock(returnValue, mocker):
    mock_execute = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = returnValue
    mock_cursor.execute = mock_execute
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor, mock_execute

class TestStr(): 
    def test_str_1(self): 
        assert RecipeModel(1, "Test", False, []).__str__() == "Test"
    
    def test_str_2(self): 
        assert RecipeModel(None, "Test2", False, []).__str__() == "Test2"

@pytest.mark.usefixtures("setup_db")
class TestGetByName(): 
    def test_found(self, conn): 
        recipe = RecipeModel.getByName("Gemüsecurry", conn)
        assert isinstance(recipe, RecipeModel)
        assert recipe.id == 2
        assert recipe.name == "Gemüsecurry"
        assert recipe.veggie == True
        assert len(recipe.ingredients) == 3
        for ingredient in recipe.ingredients: 
            assert isinstance(ingredient, IngredientForRecipeModel)
    
    def test_not_found(self, conn): 
        with pytest.raises(NameError):
            RecipeModel.getByName("asdf", conn)

    def test_mock_execution(self, mocker): 
        ### ToDo: Fix test ###
        pass

@pytest.mark.usefixtures("setup_db")
class TestGetById():
    def test_found(self, conn): 
        recipe = RecipeModel.getById("2", conn)
        assert isinstance(recipe, RecipeModel)
        assert recipe.id == 2
        assert recipe.name == "Gemüsecurry"
        assert recipe.veggie == True
        assert len(recipe.ingredients) == 3
        for ingredient in recipe.ingredients: 
            assert isinstance(ingredient, IngredientForRecipeModel)
    
    def test_not_found(self, conn): 
        with pytest.raises(NameError):
            RecipeModel.getById("999", conn)
        
    def test_invalid_id_negative(self, conn): 
        with pytest.raises(SyntaxError): 
            RecipeModel.getById(-5, conn)
    
    def test_invalid_id_no_int(self, conn): 
        with pytest.raises(SyntaxError): 
            RecipeModel.getById("asdf", conn)
    
    def test_invalid_id_empty(self, conn): 
        with pytest.raises(SyntaxError): 
            RecipeModel.getById(None, conn)

@pytest.mark.usefixtures("setup_db")
class TestGetAll(): 
    def test_success(self, conn): 
        response = RecipeModel.getAll(conn)
        assert len(response) > 0
        for recipe in response: 
            assert isinstance(recipe, RecipeModel)
    
    def test_empty(self, mocker): 
        mock_conn, mock_cursor, mock_execute = dbMock([], mocker)

        assert RecipeModel.getAll(mock_conn) == []

@pytest.mark.usefixtures("setup_db")
class TestAddRecipeEntity(): 
    def test_success(self, conn): 
        recipe = copy(test.test_constants.testRecipeModel2)
        recipe.addRecipeEntity(conn)

        assert recipe.id != None

        recipeFromDb = recipe.getById(recipe.id, conn)

        assert recipe.name == recipeFromDb.name
        assert recipe.veggie == recipeFromDb.veggie

    def test_conflict(self, conn): 
        with pytest.raises(ValueError): 
            RecipeModel(None, "Gemüsecurry", True, []).addRecipeEntity(conn)


@pytest.mark.usefixtures("setup_db")
class TestAddRelation(): 
    def test_success(self, conn): 
        recipe = RecipeModel(2, "Gemüsecurry", True, [IngredientForRecipeModel(IngredientModel(2, "Putenbrust", "g"), 500)])
        relationId = recipe.addRelation(recipe.id, recipe.ingredients[0].ingredient.id, recipe.ingredients[0].amount, conn)

        assert relationId != None

        recipeFromDb = RecipeModel.getByName(recipe.name, conn)
        for ingredient in recipeFromDb.ingredients:
            if ingredient.amount == 500 and ingredient.ingredient.name == "Putenbrust":
                found = True
        
        if found == True:
            assert True
        else: assert False
             
    def test_conflict(self, conn): 
        recipe = RecipeModel(2, "Gemüsecurry", True, [IngredientForRecipeModel(IngredientModel(5, "Broccoli", "Stk"), 1)])
        with pytest.raises(ValueError):
            recipe.addRelation(recipe.id, recipe.ingredients[0].ingredient.id, recipe.ingredients[0].amount, conn)

@pytest.mark.usefixtures("setup_db")
class TestAdd(): 
    def test_success(self, conn): 
        recipe = copy(test.test_constants.testRecipeModel2)
        recipe.add(conn)

        recipeFromDb = RecipeModel.getByName(recipe.name, conn)

        assert recipe.id == recipeFromDb.id
        assert recipe.name == recipeFromDb.name
        assert recipe.veggie == recipeFromDb.veggie
        assert len(recipe.ingredients) == len(recipeFromDb.ingredients)
    
    def test_conflicting_recipe(self, conn): 
        recipe = RecipeModel(None, "EasyTestRecipe", False, [IngredientForRecipeModel(IngredientModel(None, "TestIngredient", "g"), 1)])
        with pytest.raises(ValueError):
            recipe.add(conn)
        
    def test_existing_ingredient(self, conn): 
        recipe = RecipeModel(None, "EasyTestRecipe2", False, [IngredientForRecipeModel(IngredientModel(None, "TestIngredient", "g"), 1)])
        recipe.add(conn)

        recipeFromDb = RecipeModel.getByName(recipe.name, conn)

        assert recipe.id == recipeFromDb.id
        assert recipe.name == recipeFromDb.name
        assert recipe.veggie == recipeFromDb.veggie
        assert len(recipe.ingredients) == len(recipeFromDb.ingredients)
    
    def test_conflicting_relation(self, conn): 
        recipe = RecipeModel(None, "EasyTestRecipe2", False, 
                             [IngredientForRecipeModel(IngredientModel(None, "TestIngredient", "g"), 1),
                              IngredientForRecipeModel(IngredientModel(None, "TestIngredient", "g"), 2)])
        with pytest.raises(ValueError): 
            recipe.add(conn)

class TestDatabaseQueries(): 
    def test_query_getByName(self, mocker):
        mock_conn, mock_cursor, mock_execute = dbMock((1, "Test Recipe", True), mocker)  
        try: RecipeModel.getByName("Test Recipe", mock_conn)
        except: 
            mock_execute.assert_called_once_with("""SELECT * FROM recipes
                    LEFT JOIN recipe_ingredient_relations relations on recipes.recipeId=relations.recipeId
                    LEFT JOIN ingredients on relations.ingredientId=ingredients.ingredientId
                    WHERE recipes.recipeName = ? """, ("Test Recipe",))
    
    def test_query_getById(self, mocker):
        mock_conn, mock_cursor, mock_execute = dbMock((1, "Test Recipe", True), mocker)  
        try: RecipeModel.getById(1, mock_conn)
        except:
            mock_execute.assert_called_once_with("""SELECT * FROM recipes
                    LEFT JOIN recipe_ingredient_relations relations on recipes.recipeId=relations.recipeId
                    LEFT JOIN ingredients on relations.ingredientId=ingredients.ingredientId
                    WHERE recipes.recipeId = ? """, (1,) )
                
    def test_query_get_all(self, mocker):
        mock_conn, mock_cursor, mock_execute = dbMock([(1, "Test Recipe", True)], mocker)  
        try: RecipeModel.getAll(mock_conn)
        except: mock_execute.assert_called_once_with("""SELECT recipeId FROM recipes""")

    def test_query_add_entity(self, mocker): 
        mock_conn, mock_cursor, mock_execute = dbMock((1, "Test Recipe", True), mocker)
        RecipeModel(1, "Test Recipe", True, []).addRecipeEntity(mock_conn)
        mock_execute.assert_called_once_with("""INSERT INTO recipes (recipeName, veggie) VALUES(?, ?)""", ("Test Recipe", True))
    
    def test_query_add_relation(self, mocker): 
        mock_conn, mock_cursor, mock_execute = dbMock((1), mocker)
        RecipeModel(1, "Test Recipe", True, []).addRelation(1, 2, 500, mock_conn)
        mock_execute.assert_called_once_with("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                          (2, 1, 500))

