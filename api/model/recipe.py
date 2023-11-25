from api.model.ingredient import IngredientModel
from api.model.ingredientForRecipe import IngredientForRecipeModel
import sqlite3

conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)


class RecipeModel():
    def __init__(self, id, name, veggie, ingredients):
        self.id = id if id else None
        self.name = name
        self.veggie = veggie
        self.ingredients = ingredients

    def __str__(self):
        return self.name

    @ classmethod
    def getByName(cls, name, conn = conn):
        with conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""SELECT * FROM recipes
                    LEFT JOIN recipe_ingredient_relations relations on recipes.recipeId=relations.recipeId
                    LEFT JOIN ingredients on relations.ingredientId=ingredients.ingredientId
                    WHERE recipes.recipeName = ? """, (name,))
            rows = [dict(row) for row in c.fetchall()]
        if rows == []: raise NameError("Recipe not found")
        ingredients = [IngredientForRecipeModel(IngredientModel(row["ingredientId"], row["ingredientName"],
                                                                row["unit"]), row["amount"]) for row in rows]
        return RecipeModel(rows[0]["recipeId"], rows[0]["recipeName"], rows[0]["veggie"], ingredients)

    @classmethod
    def getById(cls, recipeId, conn = conn):
        try: i = int(recipeId)
        except: raise SyntaxError("Invalid recipeId")
        if i <= 0: raise SyntaxError("Invalid recipeId")
    
        with conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""SELECT * FROM recipes
                    LEFT JOIN recipe_ingredient_relations relations on recipes.recipeId=relations.recipeId
                    LEFT JOIN ingredients on relations.ingredientId=ingredients.ingredientId
                    WHERE recipes.recipeId = ? """, (recipeId,))
            rows = [dict(row) for row in c.fetchall()]
        if rows == []: raise NameError("Recipe not found")
        ingredients = [IngredientForRecipeModel(IngredientModel(row["ingredientId"], row["ingredientName"],
                                                                row["unit"]), row["amount"]) for row in rows]
        recipe = RecipeModel(rows[0]["recipeId"], rows[0]["recipeName"], rows[0]["veggie"], ingredients)
        return recipe

    @classmethod
    def getAll(cls, conn = conn):
        with conn:
            c = conn.cursor()
            c.execute("""SELECT recipeId FROM recipes""")
            recipes = [cls.getById(*id) for id in c.fetchall()]
            return recipes

    def addRecipeEntity(self, conn = conn):
        with conn:
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO recipes (recipeName, veggie) VALUES(?, ?)""", (self.name, self.veggie))
            except sqlite3.IntegrityError:
                raise ValueError("Recipe already exists")
            self.id = c.lastrowid
            return self
    
    def addRelation(self, recipeId, ingredientId, amount, conn = conn):
        with conn:
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                          (ingredientId, recipeId, amount))
            except sqlite3.IntegrityError:
                raise ValueError("Relation already exists")
            return c.lastrowid

    def add(self, conn = conn):
        # Add ingredients
        for recipeIngredient in self.ingredients:
            ingredient = recipeIngredient.ingredient
            try:
                ingredient.add(conn)
            except ValueError as e:
                if str(e) == "Ingredient already exists":
                    recipeIngredient.ingredient = ingredient.getByName(ingredient.name, conn)
            except:
                SyntaxError("Unknown error")

        with conn:
            # Add recipe
            try: 
                self.addRecipeEntity(conn)
            except ValueError as exception: 
                if str(exception) == "Recipe already exists": 
                    raise ValueError("Recipe already exists")
            except: 
                raise SyntaxError("Unknown error")
            
            # Add relations
            for ingredientForRecipe in self.ingredients:
                try:
                    self.addRelation(self.id, ingredientForRecipe.ingredient.id, ingredientForRecipe.amount, conn)
                except ValueError as exception:
                    if str(exception) != "Relation already exists":
                        raise SyntaxError("Unknown error")
                    else: raise ValueError("Relation already exists")
            conn.commit()
