from mongoengine import Document, StringField, EmailField
from django.contrib.auth.hashers import check_password

class User(Document):
    username = StringField(required=True, max_length=50, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, max_length=128)

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
