from mongoengine import Document, StringField, EmailField

class User(Document):
    username = StringField(required=True, max_length=50, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=128)

    def __str__(self):
        return self.username
