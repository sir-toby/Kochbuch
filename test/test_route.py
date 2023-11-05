import pytest
from pytest_mock import mocker
import api.route


from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


class TestIngredientRoute():

    def test_get_ingredients_empty_list(self, mocker):
        mocker.patch('api.route.ingredient.getAllIngredients', return_value=[])
        assert api.route.ingredient.get_ingredients() == ([], 200)

    def test_get_ingredients_exception(self, mocker):
        mocker.patch('api.route.ingredient.getAllIngredients', side_effect=Exception())
        assert api.route.ingredient.get_ingredients() == ("Unknown technical error", 500)

    def test_get_ingredients_valid(self, mocker):
        mockedIngredientsList = '[{"id": "1", "name": "testName", "unit": "g"}, {"id": "99", "name": "testIngredient", "unit": "Stk"}]'
        mocker.patch('api.route.ingredient.getAllIngredients', return_value=mockedIngredientsList)
        assert api.route.ingredient.get_ingredients() == (mockedIngredientsList, 200)
