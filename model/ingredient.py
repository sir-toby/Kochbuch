
class IngredientModel():
    def __init__(self, id, name, unit):
        self.id = id
        self.name = name
        self.unit = unit

    def __str__(self):
        return self.id + ", " + self.name + ", " + ", " + self.unit

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'unit': self.unit}
