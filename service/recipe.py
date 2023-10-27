from model.recipe import RecipeModel
from schema.recipe import RecipeSchema
import sqlite3

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)
with conn:
    c = conn.cursor()

    def getRecipeFromDatabaseByName(name):
        c.execute("""SELECT * FROM recipes WHERE name = ?""", (name))
        recipe = RecipeModel(*c.fetchone())
        return recipe_schema.dump(recipe)

    def getRecipeFromDatabaseById(recipeId):
        c.execute("""SELECT * FROM recipes WHERE id = ?""", (recipeId))
        recipe = RecipeModel(*c.fetchone())
        return recipe_schema.dump(recipe)

    def getAllRecipesFromDatabases():
        c.execute("""SELECT * FROM recipes""")
        recipes = [RecipeModel(*recipe) for recipe in c.fetchall()]
        return recipes_schema.dump(recipes)

    def addRecipeToDatabase(recipe: RecipeModel):
        try:
            c.execute("""INSERT INTO recipes (name, veggie) VALUES(?, ?)""", (recipe.name, recipe.veggie))
        except sqlite3.IntegrityError:
            raise ValueError("Entry already exists")
        conn.commit()
