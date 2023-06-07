from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Item, Shop
from ..serializers import ItemSerializer
import cloudinary
import cloudinary.uploader
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def create_item(request, shop_id):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        shop = get_object_or_404(Shop, id=shop_id)

        # Handle main image upload to Cloudinary
        image_file = request.FILES.get('image')
        if image_file:
            uploaded_image = cloudinary.uploader.upload(image_file)
            serializer.validated_data['image'] = uploaded_image['secure_url']

        # Handle detail images upload to Cloudinary
        detail_images = request.FILES.getlist('detail_image')
        uploaded_detail_images = []
        for detail_image_file in detail_images:
            uploaded_detail_image = cloudinary.uploader.upload(detail_image_file)
            uploaded_detail_images.append(uploaded_detail_image['secure_url'])

        serializer.validated_data['detail_image'] = uploaded_detail_images

        item = Item.objects.create(shop=shop, **serializer.validated_data)
        shop.items.append(item)
        shop.save()

        return Response({'success': True, 'message': 'Item created successfully'}, status=status.HTTP_201_CREATED)
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

            # Handle main image upload to Cloudinary
            image_file = request.FILES.get('image')
            if image_file:
                uploaded_image = cloudinary.uploader.upload(image_file)
                item.image = uploaded_image['secure_url']

            # Handle detail images upload to Cloudinary
            detail_images = request.FILES.getlist('detail_image')
            uploaded_detail_images = []
            for detail_image_file in detail_images:
                uploaded_detail_image = cloudinary.uploader.upload(detail_image_file)
                uploaded_detail_images.append(uploaded_detail_image['secure_url'])

            item.detail_image = uploaded_detail_images

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
        shop = item.shop
        item.delete()
        shop.items.remove(item)
        shop.save()
        return Response({'success': True, 'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'success': False, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
