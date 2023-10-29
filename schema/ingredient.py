from flask_marshmallow import Schema
from marshmallow.fields import Str, Int


class IngredientSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "amount", "unit"]

    id = Str()
    name = Str()
    amount = Int()
    unit = Str()
