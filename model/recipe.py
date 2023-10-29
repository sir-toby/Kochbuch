from model.ingredient import IngredientModel


class RecipeModel():
    def __init__(self, id, name, veggie, ingredients):
        self.id = id
        self.name = name
        self.veggie = veggie
        self.ingredients = [{IngredientModel(None, ingredient.name, ingredient.unit): ingredient.amount} for ingredient in ingredients]

    def __str__(self):
        return self.id + ", " + self.name + ", " + self.veggie

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'veggie': self.veggie}
