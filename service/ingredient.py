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
                c.execute("""INSERT INTO ingredients (name, amount, unit) VALUES(?, ?, ?)""",
                          (ingredient.name, ingredient.amount, ingredient.unit))
            except sqlite3.IntegrityError:
                raise ValueError("Ingredient already exists")
        conn.commit()
