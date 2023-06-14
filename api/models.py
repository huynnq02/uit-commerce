from mongoengine import Document, StringField, EmailField, DecimalField, DictField, ReferenceField, ListField, LazyReferenceField, BooleanField

class User(Document):
    name = StringField(required=True)
    phone_number = StringField()
    email = EmailField(required=True)
    address = StringField()
    password = StringField(required=True)
    profile_picture = StringField()
    orders = ListField(ReferenceField('Order'))
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
    colors = ListField(StringField(required=True))
    sizes = ListField(StringField(required=True))
    category = StringField(required=True)
    image = StringField(required=True)
    detail_image = ListField(StringField(required=True))
    shop = ReferenceField(Shop, reverse_delete_rule=2)
    active = BooleanField(default=True)
    
    meta = {
        'collection': 'items'  # Specify the collection name as 'items'
    }
class Order(Document):
    user = ReferenceField(User)
    shop = ReferenceField(Shop)
    items = ListField(DictField())
    status = StringField()
    address = StringField()
    total = DecimalField()
    time = StringField()
    meta = {
        'collection': 'orders'  # Specify the collection name as 'orders'
    }
class Category(Document):
    name = StringField(required=True, max_length=100)

    meta = {
        'collection': 'categories'  # Specify the collection name as 'categories'
    }
class Bill(Document):
    order = ReferenceField(Order)
    time = StringField()

    meta = {
        'collection': 'bills'  # Specify the collection name as 'bills'
    }
class Review(Document):
    item = ReferenceField(Item)
    user = ReferenceField(User)
    order = ReferenceField(Order)
    shop = ReferenceField(Shop)
    content = StringField(required=True)

    meta = {
        'collection': 'reviews'  # Specify the collection name as 'reviews'
    }
class Report(Document):
    user = ReferenceField(User)
    shop = ReferenceField(Shop)
    item = ReferenceField(Item)  # Only required if user reports a shop
    content = StringField(required=True)

    meta = {
        'collection': 'reports'  # Specify the collection name as 'reports'
    }