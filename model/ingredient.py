
class IngredientModel():
    def __init__(self, id, name, amount, unit):
        self.id = id
        self.name = name
        self.amount = amount
        self.unit = unit

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'amount': self.amount, 'unit': self.unit}
