import sqlite3

# Connect to database
conn = sqlite3.connect('../recipes.sqlite3')
c = conn.cursor()

# Create recipes table
c.execute("""CREATE TABLE recipes(
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          veggie INTEGER NOT NULL
          )""")
conn.commit()

# Create ingredients table
c.execute("""CREATE TABLE ingredients(
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL UNIQUE,
          amount REAL NOT NULL,
          unit TEXT NOT NULL
          )""")
conn.commit()

# Create relations table
c.execute("""CREATE TABLE recipe_ingredient_relations(
          id INTEGER PRIMARY KEY,
          ingredientId INTEGER NOT NULL,
          recipeId INTEGER NOT NULL,
          amount INTEGER NOT NULL,
          FOREIGN KEY(ingredientId) REFERENCES ingredients(id),
          FOREIGN KEY(recipeId) REFERENCES recipes(id)
          )""")
conn.commit()

conn.close()
