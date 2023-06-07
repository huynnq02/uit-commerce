from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from ..models import Shop, Item
import bcrypt
from ..serializers import ShopSerializer, ItemSerializer

@api_view(['POST'])
def create_shop(request):
    try:
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        shop = Shop(name=name, email=email, password=hashed_password)
        shop.save()
        return Response({'success': True, 'message': 'Shop created'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        shop.name = request.data.get('name', shop.name)
        shop.email = request.data.get('email', shop.email)
        password = request.data.get('password')
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            shop.password = hashed_password
        shop.save()
        return Response({'success': True, 'message': 'Shop updated successfully'}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        shop.delete()
        return Response({'success': True, 'message': 'Shop deleted successfully'}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_shop(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        shop = Shop.objects.get(email=email)
        is_match = bcrypt.checkpw(password.encode('utf-8'), shop.password.encode('utf-8'))
        if is_match:
            shop_data = ShopSerializer(shop).data
            # Password is correct, authentication successful
            return Response({'success': True, 'message': 'Login successful', 'data': shop_data}, status=status.HTTP_200_OK)
        else:
            # Password is incorrect
            return Response({'success': False, 'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
    except Shop.DoesNotExist:
        # Shop not found
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get all shop items
@api_view(['GET'])
def get_all_shop_items(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        items = Item.objects.filter(shop=shop)
        items_data = ItemSerializer(items, many=True).data
        return Response({'success': True, 'message': 'Shop items fetched successfully', 'data': items_data}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
