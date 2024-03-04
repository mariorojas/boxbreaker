from marshmallow import fields, Schema


class AttemptSchema(Schema):
    guess = fields.Str()
    correct = fields.Bool()
    exists = fields.Bool()
