from flask_marshmallow import Schema
from marshmallow.fields import Float, Nested
from schema.ingredient import IngredientSchema


class IngredientForRecipeSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["ingredient", "amount"]

    ingredient = Nested(IngredientSchema)
    amount = Float()
