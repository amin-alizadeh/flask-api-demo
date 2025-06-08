from app import ma
from app.models import Users, Comments, Members

from marshmallow import Schema, fields


class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users


class UsersDeserializingSchema(Schema):
    username = fields.String()
    password = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    email = fields.Email()
    birthday = fields.Date()

class MemberDeserializingSchema(Schema):
    login = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    title = fields.String()
    email = fields.Email()
    avatar_url = fields.String()
    followers = fields.Integer()
    following = fields.Integer()

class MembersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Members

class CommentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comments


class CommentsDeserializingSchema(Schema):
    body = fields.String()
    post_id = fields.Integer()
