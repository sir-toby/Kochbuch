from flask import Flask
from api.route.recipe import recipeApi
from api.route.ingredient import ingredientApi


def create_app():
    app = Flask(__name__)
    app.register_blueprint(recipeApi, url_prefix='/api/')
    app.register_blueprint(ingredientApi, url_prefix='/api/')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug="True")
