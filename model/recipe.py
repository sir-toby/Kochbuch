from model.ingredient import IngredientModel
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

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'veggie': self.veggie}

    @ classmethod
    def getByName(cls, name):
        with conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""SELECT * FROM recipes
                    LEFT JOIN recipe_ingredient_relations relations on recipes.recipeId=relations.recipeId
                    LEFT JOIN ingredients on relations.ingredientId=ingredients.ingredientId
                    WHERE recipes.recipeName = ? """, (name,))
            rows = [dict(row) for row in c.fetchall()]
        ingredients = {IngredientModel(row["ingredientId"], row["ingredientName"],
                                       row["unit"]): row["amount"] for row in rows}
        return RecipeModel(rows[0]['recipeId'], rows[0]['recipeName'], rows[0]['veggie'], ingredients)

    @classmethod
    def getById(cls, recipeId):
        with conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""SELECT * FROM recipes
                    LEFT JOIN recipe_ingredient_relations relations on recipes.recipeId=relations.recipeId
                    LEFT JOIN ingredients on relations.ingredientId=ingredients.ingredientId
                    WHERE recipes.recipeId = ? """, (recipeId,))
            rows = [dict(row) for row in c.fetchall()]
        ingredients = {IngredientModel(row["ingredientId"], row["ingredientName"],
                                       row["unit"]): row["amount"] for row in rows}
        recipe = RecipeModel(rows[0]["recipeId"], rows[0]["recipeName"], rows[0]["veggie"], ingredients)
        return recipe

    @classmethod
    def getAll(cls):
        with conn:
            c = conn.cursor()
            c.execute("""SELECT recipeId FROM recipes""")
            recipes = [cls.getById(*id) for id in c.fetchall()]
            return recipes

    def addRecipeEntity(self):
        with conn:
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO recipes (recipeName, veggie) VALUES(?, ?)""", (self.name, self.veggie))
            except sqlite3.IntegrityError:
                raise ValueError("Recipe already exists")
            self.id = c.lastrowid
            return self

    def addRelation(recipeId, ingredientId, amount):
        with conn:
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO recipe_ingredient_relations (ingredientId, recipeId, amount) VALUES(?, ?, ?)""",
                          (ingredientId, recipeId, amount))
            except sqlite3.IntegrityError:
                raise ValueError("Relation already exists")
            return c.lastrowid

    def add(self):
        # Add ingredients
        for ingredient in self.ingredients:
            try:
                ingredient.add()
            except ValueError as e:
                if str(e) == "Ingredient already exists":
                    ingredient = ingredient.getByName(ingredient.name)
            except:
                ValueError("Unknown error")

        with conn:
            # Add recipe
            self.addRecipeEntity()

            # Add relations
            for ingredient in self.ingredients:
                try:
                    self.addRelation(self.id, ingredient.id, self.ingredients[ingredient])
                except ValueError as exception:
                    if str(exception) != "Relation already exists":
                        raise SyntaxError("Unknown error")
            conn.commit()
