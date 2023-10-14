import sqlite3


class Recipe():
    def __init__(self, id, name, veggie):
        self.id = id
        self.name = name
        self.veggie = veggie

    def __str__(self):
        return self.id + ", " + self.name + ", " + self.veggie

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'veggie': self.veggie}

    def addToDatabase(self):
        conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)
        with conn:
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO recipes (name, veggie) VALUES(?, ?)""", (self.name, self.veggie))
            except sqlite3.IntegrityError:
                raise ValueError("Entry already exists")
            conn.commit()


class Ingredient():
    def __init__(self, id, name, amount, unit):
        self.id = id
        self.name = name
        self.amount = amount
        self.unit = unit

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'amount': self.amount, 'unit': self.unit}
