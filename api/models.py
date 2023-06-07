from mongoengine import Document, StringField, EmailField, DecimalField, ImageField, ReferenceField, ListField, LazyReferenceField, BooleanField

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
    name = StringField(max_length=100, required=True)
    hotline = StringField()
    email = EmailField(required=True)
    address = StringField()
    password = StringField(required=True)
    items = ListField(ReferenceField('Item'))

    meta = {
        'collection': 'shops'  # Specify the collection name as 'shops'
    }

class Item(Document):
    name = StringField(required=True, max_length=100)
    price = DecimalField(required=True, precision=2)
    discount = DecimalField(required=True, precision=2)
    quantity = DecimalField(required=True)
    description = StringField(required=True)
    color = ListField(StringField(required=True, max_length=50))
    size = ListField(StringField(required=True, max_length=10))
    category = StringField(required=True)
    image = ImageField(required=True)
    detail_image = ListField(ImageField(required=True))
    shop = LazyReferenceField(Shop, required=True, reverse_delete_rule=2)
    active = BooleanField(default=True)
    
    meta = {
        'collection': 'items'  # Specify the collection name as 'items'
    }
