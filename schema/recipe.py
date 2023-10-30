from flask_marshmallow import Schema
from marshmallow.fields import Str, Bool, Nested
from schema.ingredient import IngredientSchema


class RecipeSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "veggie", "ingredients"]

    id = Str()
    name = Str()
    veggie = Bool()
    ingredients = Nested(IngredientSchema, many=True)
