from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from ..models import Shop, Item, User, Order
import bcrypt
from ..serializers import ShopSerializer, ItemSerializer, UserSerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

@api_view(['POST'])
def create_shop(request):
    """
    Create a new shop.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the status of the shop creation.

    Raises:
        Exception: If any error occurs during the shop creation.

    """
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
    """
    Update a shop.

    Args:
        request (HttpRequest): The HTTP request object.
        shop_id (int): The ID of the shop to update.

    Returns:
        Response: The HTTP response containing the status of the shop update.

    Raises:
        Shop.DoesNotExist: If the shop with the specified ID does not exist.
        Exception: If any error occurs during the shop update.

    """
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
    """
    Delete a shop.

    Args:
        request (HttpRequest): The HTTP request object.
        shop_id (int): The ID of the shop to delete.

    Returns:
        Response: The HTTP response containing the status of the shop deletion.

    Raises:
        Shop.DoesNotExist: If the shop with the specified ID does not exist.
        Exception: If any error occurs during the shop deletion.

    """
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
    """
    Authenticate a shop.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the status of the shop authentication.

    Raises:
        Shop.DoesNotExist: If the shop with the specified email does not exist.
        Exception: If any error occurs during the shop authentication.

    """
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
def get_all_shop_items(request, id):
    """
    Retrieve all items of a shop.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the shop.

    Returns:
        Response: The HTTP response containing the shop items data.

    Raises:
        Shop.DoesNotExist: If the shop with the specified ID does not exist.
        Exception: If any error occurs while retrieving the shop items.

    """
    try:
        shop = Shop.objects.get(id=id)
        items = Item.objects.filter(shop=shop)
        items_data = ItemSerializer(items, many=True).data
        return Response({'success': True, 'message': 'Shop items fetched successfully', 'data': items_data}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def get_list_customers(request, id):
    """
    Retrieve user information, number of orders, and number of bills for each user associated with a given shop.

    Args:
        request (HttpRequest): The HTTP request object.
        id (str): The ID of the shop.

    Returns:
        Response: A response object containing the result of the operation.

    Raises:
        Shop.DoesNotExist: If the shop with the specified ID does not exist.
        Exception: If any other error occurs during the process.

    """
    try:
        shop = Shop.objects.get(id=id)

        user_ids = [order.user.id for order in Order.objects.filter(shop=shop)]
        users = User.objects.filter(id__in=user_ids)
        
        user_info = []
        for user in users:
            orders = Order.objects.filter(user=user, shop=shop)
            total_orders = orders.count()
            total_bills = sum(order.total for order in orders)

            user_data = {
                'user': {
                    'id': str(user.id),
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'address': user.address,
                    'password': user.password,
                    'profile_picture': user.profile_picture,
                    'orders': user.orders,
                    'num_orders': total_orders,
                    'total_bills': total_bills
                },  
            }
            user_info.append(user_data)

        return Response({'success': True, 'message': 'Shop user information fetched successfully', 'data': user_info}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_statistics(request, shop_id):
    """
    Retrieve statistics for a shop.

    Args:
        request (HttpRequest): The HTTP request object.
        shop_id (int): The ID of the shop.

    Returns:
        Response: The HTTP response containing the shop statistics data.

    Raises:
        Shop.DoesNotExist: If the shop with the specified ID does not exist.
        Exception: If any error occurs while retrieving the shop statistics.

    """
    try:
        shop = Shop.objects.get(id=shop_id)
        current_time = datetime.now()
        start_date = current_time - relativedelta(months=5)
        start_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Include the current month in the range
        end_date = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + relativedelta(months=1)

        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        sales_last_six_months = {name: 0 for name in month_names}
        print("current:",current_time)
        print("start:",start_date)
        print("end:",end_date)

        orders = Order.objects.filter(shop=shop)
        for order in orders:
            order_time = datetime.strptime(order.time[:19], "%Y-%m-%dT%H:%M:%S")
            print("order_time:",order_time)
            print()
            if start_date <= order_time <= end_date:
                order_month = order_time.month
                month_name = month_names[order_month - 1]
                sales_last_six_months[month_name] += order.total
                print("order_month:",order_month)
                print("order.total:",order.total)	
                print("month_name:",month_name)
                print("sales_last_six_months:",sales_last_six_months)
        # Calculate the total sales for today
        today_sales = Order.objects.filter(shop=shop)
        total_sales_today = sum(order.total for order in today_sales if datetime.strptime(order.time[:19], "%Y-%m-%dT%H:%M:%S").date() == current_time.date())

        # Calculate the total sales for the last week
        last_week_sales = Order.objects.filter(shop=shop)
        total_sales_last_week = sum(order.total for order in last_week_sales if (current_time - timedelta(days=7)).date() <= datetime.strptime(order.time[:19], "%Y-%m-%dT%H:%M:%S").date() < current_time.date())

        # Calculate the total sales for the last month
        last_month_sales = Order.objects.filter(shop=shop)
        total_sales_last_month = sum(order.total for order in last_month_sales if (current_time - relativedelta(months=1)).date() <= datetime.strptime(order.time[:19], "%Y-%m-%dT%H:%M:%S").date() < current_time.date())

        data = {
            "sales_last_six_months": sales_last_six_months,
            "total_sales_today": total_sales_today,
            "total_sales_last_week": total_sales_last_week,
            "total_sales_last_month": total_sales_last_month
        }

        return Response({'success': True, 'message': 'Statistics fetched successfully', 'data': data}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)