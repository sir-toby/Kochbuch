import sqlite3

conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)


class IngredientForRecipeModel():
    def __init__(self, ingredient, amount):
        self.ingredient = ingredient
        self.amount = amount

    def __str__(self):
        return self.ingredient + ", " + self.amount
