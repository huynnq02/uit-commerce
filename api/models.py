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
    price = DecimalField(required=True, precision=2, min_value=0)
    discount = DecimalField(required=True, precision=2, min_value=0)
    quantity = DecimalField(required=True, min_value=0)
    description = StringField(required=True)
    color = ListField(StringField(required=True))
    size = ListField(StringField(required=True))
    category = StringField(required=True)
    image = StringField(required=True)
    detail_image = ListField(StringField(required=True))
    shop = ReferenceField(Shop, reverse_delete_rule=2)
    active = BooleanField(default=True)
    
    meta = {
        'collection': 'items'  # Specify the collection name as 'items'
    }
