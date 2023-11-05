import sqlite3

conn = sqlite3.connect('recipes.sqlite3', check_same_thread=False)


class IngredientModel():
    def __init__(self, id, name, unit):
        self.id = id if id else None
        self.name = name
        self.unit = unit

    def __str__(self):
        return self.name + ", " + self.unit

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'unit': self.unit}

    @classmethod
    def getByName(cls, name):
        with conn:
            c = conn.cursor()
            c.execute("""SELECT * FROM ingredients WHERE ingredientName = ?""", (name,))
            return IngredientModel(*c.fetchone())

    @classmethod
    def getById(cls, ingredientId):
        with conn:
            c = conn.cursor()
            c.execute("""SELECT * FROM ingredients WHERE ingredientId = ?""", (ingredientId,))
            return IngredientModel(*c.fetchone())

    @classmethod
    def getAll(cls):
        with conn:
            c = conn.cursor()
            c.execute("""SELECT * FROM ingredients""")
            return [IngredientModel(*ingredient) for ingredient in c.fetchall()]

    def add(self):
        with conn:
            c = conn.cursor()
            try:
                c.execute("""INSERT INTO ingredients (ingredientName, unit) VALUES(?, ?)""",
                          (self.name, self.unit))
            except sqlite3.IntegrityError:
                raise ValueError("Ingredient already exists")
            self.id = c.lastrowid
            conn.commit()
        return self
