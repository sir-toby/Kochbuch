import pytest
from pytest_mock import mocker
from unittest.mock import MagicMock
import sqlite3

from infrastructure.db_setup import create_database
from infrastructure.createTestData import createTestData

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
        assert IngredientModel(1, "Test", "g").__str__() == "Test, g"
    
    def test_str_2(self): 
        assert IngredientModel(None, "Broccoli", "Pcs").__str__() == "Broccoli, Pcs"

@pytest.mark.usefixtures("setup_db")
class TestGetByName(): 
    def test_found(self, conn): 
        ingredient = IngredientModel.getByName("Ei", conn)
        assert ingredient.id == 4
        assert ingredient.name == "Ei"
        assert ingredient.unit == "Stk"
    
    def test_not_found(self, conn): 
        with pytest.raises(NameError):
            IngredientModel.getByName("asdf", conn)


@pytest.mark.usefixtures("setup_db")
class TestGetById():
    def test_found(self, conn): 
        ingredient = IngredientModel.getById("4", conn)
        assert ingredient.name == "Ei"
        assert ingredient.unit == "Stk"
    
    def test_not_found(self, conn): 
        with pytest.raises(NameError):
            IngredientModel.getById("999", conn)
        
    def test_invalid_id_negative(self, conn): 
        with pytest.raises(SyntaxError): 
            IngredientModel.getById(-5, conn)

    def test_invalid_id_string(self, conn): 
        with pytest.raises(SyntaxError): 
            IngredientModel.getById("asdf", conn)
    
    def test_invalid_id_empty(self, conn): 
        with pytest.raises(SyntaxError): 
            IngredientModel.getById(None, conn)
    
    def test_query_execution(self, mocker):
        mock_execute = mocker.MagicMock()
        mock_cursor = mocker.MagicMock()
        mock_cursor.fetchone.return_value = (1, "Test Ingredient", "grams")
        mock_cursor.execute = mock_execute
        mock_conn = mocker.MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        ingredient = IngredientModel.getById(1, mock_conn)
        
        mock_execute.assert_called_once_with(
            "SELECT * FROM ingredients WHERE ingredientId = ?", 
            (1,)
        )

@pytest.mark.usefixtures("setup_db")
class TestGetAll(): 
    def test_success(self, conn): 
        response = IngredientModel.getAll(conn)
        assert len(response) > 0
        for ingredient in response: 
            assert isinstance(ingredient, IngredientModel)
    

@pytest.mark.usefixtures("setup_db")
class TestAdd(): 
    def test_success(self, conn): 
        ingredient = IngredientModel(None, "TestIngredient99", "g")
        ingredient.add(conn)

        assert ingredient.id != None
        
        ingredientFromDb = IngredientModel.getByName("TestIngredient99", conn)

        assert ingredient.id == ingredientFromDb.id
        assert ingredient.name == ingredientFromDb.name
        assert ingredient.unit == ingredientFromDb.unit

    def test_conflict(self, conn): 
        with pytest.raises(ValueError): 
            IngredientModel(None, "Ei", "Stk").add(conn)



class TestDbExecutions(): 
    def test_query_get_by_name(self, mocker):
        mock_conn, mock_cursor, mock_execute = dbMock((1, "Test Ingredient", "grams"), mocker)  
        ingredient = IngredientModel.getByName("Test Ingredient", mock_conn)
        
        mock_execute.assert_called_once_with(
            "SELECT * FROM ingredients WHERE ingredientName = ?", 
            ("Test Ingredient",)
        )
    
    def test_query_get_by_id(self, mocker): 
        mock_conn, mock_cursor, mock_execute = dbMock((1, "Test Ingredient", "grams"), mocker)  
        ingredient = IngredientModel.getById(1, mock_conn)
        
        mock_execute.assert_called_once_with(
            "SELECT * FROM ingredients WHERE ingredientId = ?", 
            (1,)
        )
    
        
    def test_query_get_all(self, mocker): 
        mock_conn, mock_cursor, mock_execute = dbMock([(1, "Test Ingredient", "grams")], mocker)  
        ingredient = IngredientModel.getAll(mock_conn)
        
        mock_execute.assert_called_once_with(
            "SELECT * FROM ingredients"
        )
    
    
    def test_query_add(self, mocker): 
        mock_conn, mock_cursor, mock_execute = dbMock((1, "Test Ingredient", "grams"), mocker)  
        ingredient = IngredientModel(1, "Test Ingredient", "grams").add(mock_conn)

        mock_execute.assert_called_once_with(
            """INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""",
            ("Test Ingredient", "grams"))
