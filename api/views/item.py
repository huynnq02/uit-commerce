from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Item, Shop
import cloudinary
import cloudinary.uploader
from ..serializers import ItemSerializer
from decimal import Decimal
from utils.CustomPagination import CustomPagination

@api_view(['POST'])
def create_item(request, shop_id):
    data = request.data

    try:
        shop = Shop.objects.get(id=shop_id)
        print(1)
        required_fields = ['name', 'price', 'discount', 'quantity', 'description', 'colors', 'sizes', 'category']
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
        print(2)

        # Handle main image upload to Cloudinary
        image_file = request.FILES.get('image')
        print(image_file)
        if image_file:
            uploaded_image = cloudinary.uploader.upload(image_file)
            image_url = uploaded_image['secure_url']
        else:
            image_url = ''

        # Handle detail images upload to Cloudinary
        detail_images = request.FILES.getlist('detail_image')
        print(detail_images)
        uploaded_detail_images = []
        for detail_image_file in detail_images:
            uploaded_detail_image = cloudinary.uploader.upload(detail_image_file)
            uploaded_detail_images.append(uploaded_detail_image['secure_url'])
        print(3)

        item_data = {
            'name': data['name'],
            'price': price,
            'discount': discount,
            'quantity': quantity,
            'description': data['description'],
            'colors': [colors.strip() for colors in data['colors'].split(',')],
            'sizes': [sizes.strip() for sizes in data['sizes'].split(',')],  # Convert to list
            'category': data['category'],
            'image': image_url,
            'detail_image': uploaded_detail_images,
            'shop': str(shop.id),  # Convert Shop object to its ID
            'active': True
        }
        print(4)

        item = Item(**item_data)
        print(5)
        item.save()
        print(6)

        shop.items.append(item)
        print(7)
        shop.save()
        print(8)

        item_data['image'] = str(item_data['image'])
        item_data['detail_image'] = [str(image) for image in item_data['detail_image']]
        print(6)

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



@api_view(['GET'])
def get_all_items(request):
    try:
        paginator = CustomPagination()
        items = Item.objects.all()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)