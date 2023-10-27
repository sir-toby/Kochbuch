from flask_marshmallow import Schema
from marshmallow.fields import Str, Bool


class RecipeSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["id", "name", "veggie"]

    id = Str()
    name = Str()
    veggie = Bool()
