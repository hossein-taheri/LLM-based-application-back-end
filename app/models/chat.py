import mongoengine as me


class ChatMessage(me.EmbeddedDocument):
    text = me.StringField(required=True)
    is_users = me.BooleanField(required=True)
    created_at = me.DateTimeField()


class Chat(me.Document):
    user_id = me.ObjectIdField(required=True)
    messages = me.EmbeddedDocumentListField(document_type=ChatMessage, required=True)
    created_at = me.DateField(required=True)
