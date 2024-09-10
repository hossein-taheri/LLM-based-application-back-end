import mongoengine as me
import bcrypt


class User(me.Document):
    email = me.StringField(required=True, unique=True)
    password_hash = me.StringField(required=True)
    salt = me.StringField(required=True)
    created_at = me.DateField(required=True)

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8'), salt.decode('utf-8')

    @staticmethod
    def check_password(password, password_hash, salt):
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
