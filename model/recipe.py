class RecipeModel():
    def __init__(self, id, name, veggie):
        self.id = id
        self.name = name
        self.veggie = veggie

    def __str__(self):
        return self.id + ", " + self.name + ", " + self.veggie

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'veggie': self.veggie}
