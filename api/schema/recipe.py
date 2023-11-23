from flask_marshmallow import Schema
from marshmallow.fields import Str, Bool, Nested, Mapping, Float
from api.schema.ingredientForRecipe import IngredientForRecipeSchema


class RecipeSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "veggie", "ingredients"]

    id = Str()
    name = Str()
    veggie = Bool()
    ingredients = Nested(IngredientForRecipeSchema, many=True)
