from mongoengine import Document, StringField, IntField,ReferenceField

class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    email = StringField(max_length=100, required=True, unique=True)
    password = StringField(max_length=100, required=True)
    meta = {'collection': 'Users'}

class Crud(Document):
    task=StringField(max_length=200, required=True)
    user=ReferenceField(User, required=True)
    meta = {'collection': 'crud_tasks'}