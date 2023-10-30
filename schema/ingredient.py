from flask_marshmallow import Schema
from marshmallow.fields import Str, Float


class IngredientSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "unit", "amount"]

    id = Str()
    name = Str()
    unit = Str()
    amount = Float()
