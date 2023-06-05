from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Shop
from ..serializers import ShopSerializer, ItemSerializer

@api_view(['POST'])
def create_shop(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')

    shop_data = {'name': name, 'email': email, 'password': password}
    serializer = ShopSerializer(data=shop_data)
    if serializer.is_valid():
        serializer.save()
        return Response({ 'success': True, 'message' : "Shop created"}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success' : False, 'message' : "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ShopSerializer(shop, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        shop.delete()
        return Response({'success': True, 'message': 'Shop deleted successfully'}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login_shop(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        shop = Shop.objects.get(email=email, password=password)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_shop_items(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        items = shop.item_set.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)