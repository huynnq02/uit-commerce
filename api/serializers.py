from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import User, Item, Shop, Order, Category, Report, Review, Bill

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

class CategorySerializer(DocumentSerializer):
    class Meta:
        model = Category

class BillSerializer(DocumentSerializer):
    order = OrderSerializer()

    class Meta:
        model = Bill

class ReviewSerializer(DocumentSerializer):
    item = ItemSerializer()
    user = UserSerializer()
    order = OrderSerializer()
    shop = ShopSerializer()

    class Meta:
        model = Review
        
class ReportSerializer(DocumentSerializer):
    user = UserSerializer()
    shop = ShopSerializer()
    item = ItemSerializer()

    class Meta:
        model = Report

