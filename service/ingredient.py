from model.ingredient import IngredientModel
from schema.ingredient import IngredientSchema
import sqlite3

ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)


conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)
with conn:
    c = conn.cursor()

    def getIngredientFromDatabaseByName(name):
        c.execute("""SELECT * FROM ingredients WHERE name = ?""", (name))
        ingredient = IngredientModel(*c.fetchone())
        return ingredient_schema.dump(ingredient)

    def getIngredientFromDatabaseById(ingredientId):
        c.execute("""SELECT * FROM ingredients WHERE id = ?""", (ingredientId))
        ingredient = IngredientModel(*c.fetchone())
        return ingredient_schema.dump(ingredient)

    def getAllIngredientsFromDatabase():
        c.execute("""SELECT * FROM ingredients""")
        ingredients = [IngredientModel(*ingredient) for ingredient in c.fetchall()]
        return ingredients_schema.dump(ingredients)

    def addIngredientsToDatabase(ingredients):
        for ingredient in ingredients:
            try:
                addIngredientToDatabase(*ingredient.keys())
            except ValueError as exception:
                if str(exception) != "Ingredient already exists":
                    raise ValueError(str(exception))
        return

    def addIngredientToDatabase(ingredient):
        try:
            c.execute("""INSERT INTO ingredients (name, unit) VALUES(?, ?)""",
                      (ingredient.name, ingredient.unit))
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Ingredient already exists")
        ingredient.id = c.lastrowid
        conn.commit()
