from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import User, Item

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User

class ItemSerializer(DocumentSerializer):
    class Meta:
        model = Item