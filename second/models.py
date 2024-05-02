from mongoengine import *


class Contact(Document):
    name = StringField(max_length=150)
    email = StringField(max_length=150)
    sent = BooleanField(default=False)
