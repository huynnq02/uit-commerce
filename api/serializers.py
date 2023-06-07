from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import User, Item, Shop

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
