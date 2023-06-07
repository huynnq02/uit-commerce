from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Item, Shop
import cloudinary
import cloudinary.uploader

from decimal import Decimal


@api_view(['POST'])
def create_item(request, shop_id):
    data = request.data

    try:
        shop = Shop.objects.get(id=shop_id)

        required_fields = ['name', 'price', 'discount', 'quantity', 'description', 'color', 'size', 'category']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert price, discount, and quantity to decimal
        try:
            price = Decimal(data['price'])
            discount = Decimal(data['discount'])
            quantity = Decimal(data['quantity'])
        except (ValueError, TypeError, Decimal.InvalidOperation):
            return Response({'success': False, 'message': 'Invalid decimal values'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle main image upload to Cloudinary
        image_file = request.FILES.get('image')
        if image_file:
            uploaded_image = cloudinary.uploader.upload(image_file)
            image_url = uploaded_image['secure_url']
        else:
            image_url = ''

        # Handle detail images upload to Cloudinary
        detail_images = request.FILES.getlist('detail_image')
        uploaded_detail_images = []
        for detail_image_file in detail_images:
            uploaded_detail_image = cloudinary.uploader.upload(detail_image_file)
            uploaded_detail_images.append(uploaded_detail_image['secure_url'])

        item_data = {
            'name': data['name'],
            'price': price,
            'discount': discount,
            'quantity': quantity,
            'description': data['description'],
            'color': [color.strip() for color in data['color'].split(',')],
            'size': [size.strip() for size in data['size'].split(',')],  # Convert to list
            'category': data['category'],
            'image': image_url,
            'detail_image': uploaded_detail_images,
            'shop': str(shop.id),  # Convert Shop object to its ID
            'active': True
        }

        item = Item(**item_data)
        item.save()

        shop.items.append(item)
        shop.save()

        item_data['image'] = str(item_data['image'])
        item_data['detail_image'] = [str(image) for image in item_data['detail_image']]

        return Response({'success': True, 'message': 'Item created successfully', 'data': item_data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_item(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response({'success': False, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    shop_id = data.get('shop')

    try:
        shop = Shop.objects.get(id=shop_id)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

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
