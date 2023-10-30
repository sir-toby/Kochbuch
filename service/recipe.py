from model.recipe import RecipeModel
from schema.recipe import RecipeSchema
from service.ingredient import addIngredientsToDatabase
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

    def getAllRecipesFromDatabase():
        c.execute("""SELECT * FROM recipes""")
        recipes = [RecipeModel(*recipe) for recipe in c.fetchall()]
        return recipes_schema.dump(recipes)

    def addRecipeToDatabase(recipe: RecipeModel):
        try:
            print(recipe.name)
            c.execute("""INSERT INTO recipes (name, veggie) VALUES(?, ?)""", (recipe.name, recipe.veggie))
        except sqlite3.IntegrityError:
            raise ValueError("Recipe already exists")
        return c.lastrowid()

    def addRelationToDatabase(recipeId, ingredientId, amount):
        try:
            c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                      (ingredientId, recipeId, amount))
        except sqlite3.IntegrityError:
            raise ValueError("Relation already exists")
        return c.lastrowid()

    def addRecipe(jsonRecipe):
        try:
            veggie = jsonRecipe["veggie"]
        except:
            veggie = False
        recipe = RecipeModel(None, jsonRecipe["name"], veggie, jsonRecipe["ingredients"])

        # Add ingredients
        addIngredientsToDatabase(recipe.ingredients)

        # Add recipe
        recipe.id = addRecipeToDatabase(recipe)

        # Add relations
        for ingredient in recipe.ingredients:
            try:
                addRelationToDatabase(recipe.id, ingredient.id, recipe.ingredients[ingredient])
            except ValueError as exception:
                if str(exception) != "Relation already exists":
                    raise SyntaxError("Unknown error")
        conn.commit()
