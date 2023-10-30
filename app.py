
from flask import Flask
from route.recipe import recipeApi
from route.ingredient import ingredientApi


def create_app():
    app = Flask(__name__)
    app.register_blueprint(recipeApi, url_prefix='/')
    app.register_blueprint(ingredientApi, url_prefix='/')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug="True")
