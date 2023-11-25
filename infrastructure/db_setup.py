import sqlite3
from os import getcwd

# Connect to database
def create_database(conn):
    
    c = conn.cursor()

    # Create recipes table
    c.execute("""CREATE TABLE recipes(
            recipeId INTEGER PRIMARY KEY,
            recipeName TEXT NOT NULL UNIQUE,
            veggie INTEGER NOT NULL
            )""")
    conn.commit()

    # Create ingredients table
    c.execute("""CREATE TABLE ingredients(
            ingredientId INTEGER PRIMARY KEY,
            ingredientName TEXT NOT NULL UNIQUE,
            unit TEXT NOT NULL
            )""")
    conn.commit()

    # Create relations table
    c.execute("""CREATE TABLE recipe_ingredient_relations(
            relationId INTEGER PRIMARY KEY,
            ingredientId INTEGER NOT NULL,
            recipeId INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY(ingredientId) REFERENCES ingredients(id),
            FOREIGN KEY(recipeId) REFERENCES recipes(id),
            CONSTRAINT unique_relation UNIQUE(ingredientId, recipeId)
            )""")
    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(getcwd() + '/recipes.sqlite3')
    create_database(conn)
    conn.close()