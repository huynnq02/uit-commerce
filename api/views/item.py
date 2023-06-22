from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Item, Shop, User, Order
import cloudinary
import cloudinary.uploader
from ..serializers import ItemSerializer
from decimal import Decimal
from utils.CustomPagination import CustomPagination

@api_view(['POST'])
def create_item(request, shop_id):
    """
    Create a new item.

    Args:
        request (HttpRequest): The HTTP request object.
        shop_id (int): The ID of the shop to which the item belongs.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Shop.DoesNotExist: If the shop with the specified ID does not exist.
        Exception: If any error occurs while creating the item.

    """
    data = request.data

    try:
        shop = Shop.objects.get(id=shop_id)
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
    
        # Handle main image upload to Cloudinary
        image_file = request.FILES.get('image')

        if image_file:
            uploaded_image = cloudinary.uploader.upload(image_file)
            image_url = uploaded_image['secure_url']
        else:
            image_url = ''

        # Handle detail images upload to Cloudinary
        detail_images = [request.FILES.get(f'detail_image[{index}]') for index in range(len(request.FILES)) if f'detail_image[{index}]' in request.FILES]
        print(detail_images)
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
            'colors': [colors.strip() for colors in data['colors'].split(',')],
            'sizes': [sizes.strip() for sizes in data['sizes'].split(',')],  # Convert to list
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
    """
    Update an existing item.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the item to update.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Item.DoesNotExist: If the item with the specified ID does not exist.
        Exception: If any error occurs while updating the item.

    """
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return Response({'success': False, 'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    if 'name' in data:
        item.name = data['name']
    if 'price' in data:
        item.price = data['price']
    if 'discount' in data:
        item.discount = data['discount']
    if 'quantity' in data:
        item.quantity = data['quantity']
    if 'description' in data:
        item.description = data['description']
    if 'colors' in data:
        item.colors = data['colors']
    if 'sizes' in data:
        item.sizes = data['sizes']
    if 'category' in data:
        item.category = data['category']
    if 'active' in data:
        item.active = data['active']

    item.save()
    return Response({'success': True, 'message': 'Item updated successfully'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_item(request, id):
    """
    Delete an item.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the item to delete.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Item.DoesNotExist: If the item with the specified ID does not exist.
        Exception: If any error occurs while deleting the item.

    """
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
def check_item_bought(request, user_id, item_id):
    """
    Check if an item has been bought by a user.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user.
        item_id (int): The ID of the item.

    Returns:
        Response: The HTTP response indicating whether the item has been bought by the user or not.

    Raises:
        User.DoesNotExist: If the user with the specified ID does not exist.
        Order.DoesNotExist: If no orders exist for the item.

    """
    try:
        user = User.objects.get(id=user_id)
        # get orther that has item_id
        orders = Order.objects.filter(items__id=item_id)
        print(orders)
        for order in orders:

            if order.user == user:
                return Response({'success': True, 'message': 'Item bought before', 'data': True }, status= 200)
        return Response({'success': True, 'message': 'Item not bought before', 'data': False }, status= 200)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User not found'}, status = 404)
    except Order.DoesNotExist:
        return Response({'success': False, 'message': 'Order not found'}, status = 404)


@api_view(['GET'])
def get_all_items(request):
    """
    Get all items.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The paginated HTTP response containing the items.

    Raises:
        Exception: If any error occurs while retrieving the items.

    """
    try:
        paginator = CustomPagination()
        items = Item.objects.all()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            'success': True,
            'message': 'Items retrieved successfully',
            'data': serializer.data
        })
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)