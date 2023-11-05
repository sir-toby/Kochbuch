from flask_marshmallow import Schema
from marshmallow.fields import Str


class IngredientSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "unit"]

    id = Str()
    name = Str()
    unit = Str()
