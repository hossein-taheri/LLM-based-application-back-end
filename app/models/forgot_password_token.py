import mongoengine as me
from app.models.user import User
from datetime import datetime


class ForgotPasswordToken(me.Document):
    user = me.ReferenceField(User, required=True)
    token = me.StringField(required=True, unique=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    expires_at = me.DateTimeField(required=True)
