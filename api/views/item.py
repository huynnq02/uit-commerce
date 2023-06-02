from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Item, Shop
from ..serializers import ItemSerializer

@api_view(['POST'])
def create_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        shop_id = request.data.get('shop')
        try:
            shop = Shop.objects.get(id=shop_id)
            item = Item(shop=shop, **serializer.validated_data)
            item.save()
            return Response({'success': True, 'message': 'Item created successfully'}, status=status.HTTP_201_CREATED)
        except Shop.DoesNotExist:
            return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response({'success': False, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        shop_id = request.data.get('shop')
        try:
            shop = Shop.objects.get(id=shop_id)
            item.shop = shop
            item.save()
            return Response({'success': True, 'message': 'Item updated successfully'}, status=status.HTTP_200_OK)
        except Shop.DoesNotExist:
            return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_item(request, id):
    try:
        item = Item.objects.get(id=id)
        item.delete()
        return Response({'success': True, 'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'success': False, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)