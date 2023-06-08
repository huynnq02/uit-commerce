from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import User, Item, Shop, Order

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User

class ShopSerializer(DocumentSerializer):
    class Meta:
        model = Shop
 
class ItemSerializer(DocumentSerializer):
    shop = ShopSerializer()
    class Meta:
        model = Item
class OrderSerializer(DocumentSerializer):
    user = UserSerializer()
    shop = ShopSerializer
    item = ItemSerializer
    class Meta:
        model = Order