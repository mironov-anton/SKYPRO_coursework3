from marshmallow import fields, Schema


class MovieSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()
