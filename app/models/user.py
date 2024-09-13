import uuid

import mongoengine as me
import bcrypt


class User(me.Document):
    email = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    salt = me.StringField(required=True)
    verification_token = me.StringField(required=False)
    verified_email_at = me.DateTimeField(required=False)
    created_at = me.DateTimeField(required=True)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8'), salt.decode('utf-8')

    @staticmethod
    def check_password(password, password_hash, salt):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())
