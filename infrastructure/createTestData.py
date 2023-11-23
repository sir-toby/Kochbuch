import sqlite3
from os import getcwd

def createTestData(databaseName):
    # Connect to database
    conn = sqlite3.connect(getcwd() + '/' + databaseName)
    c = conn.cursor()

    with conn:
        # Recipes
        c.execute("""INSERT INTO recipes (recipeName, veggie) VALUES(?, ?)""", ("Röstischnitzel", False))
        c.execute("""INSERT INTO recipes (recipeName, veggie) VALUES(?, ?)""", ("Gemüsecurry", True))

        # Ingredients
        c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""", ("Berner Rösti", "g"))
        c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""", ("Putenbrust", "g"))
        c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""", ("Reibekäse", "g"))
        c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""", ("Ei", "Stk"))
        c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""", ("Broccoli", "Stk"))
        c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""", ("Currypaste", "EL"))

        # Relations
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (1, 1, 500))
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (2, 1, 500))
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (3, 1, 200))
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (4, 1, 2))
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (4, 2, 2))
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (5, 2, 2))
        c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                (6, 2, 2))

if __name__ == "__main__":
    createTestData('recipes.sqlite3')