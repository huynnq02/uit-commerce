from mongoengine import Document, StringField, EmailField, DecimalField, ImageField, ReferenceField
class User(Document):
    name = StringField(required=True)
    phone_number = StringField()
    email = EmailField(required=True)
    address = StringField()
    password = StringField(required=True)
    meta = {
        'collection': 'users'  # Specify the collection name as 'users'
    }

class Shop(Document):
    name = StringField(max_length=100)
    meta = {
        'collection': 'shops'  # Specify the collection name as 'shops'
    }
class Item(Document):
    name = StringField(required=True, max_length=100)
    price = DecimalField(required=True, precision=2)
    discount = DecimalField(required=True, precision=2)
    description = StringField(required=True)
    color = StringField(required=True, max_length=50)
    dimension = StringField(required=True, max_length=10)
    image = ImageField(required=True)
    shop = ReferenceField(Shop)
    meta = {
        'collection': 'items'  # Specify the collection name as 'items'
    }