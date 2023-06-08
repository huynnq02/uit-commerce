from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Order
from ..serializers import OrderSerializer


@api_view(['POST'])
def create_order(request):
    try:
        user_id = request.data.get('user_id')
        shop_id = request.data.get('shop_id')
        item_id = request.data.get('item_id')
        time = request.data.get('time')
        status = request.data.get('status')

        order = Order(user=user_id, shop=shop_id, item=item_id, time=time, status=status)
        order.save()

        return Response({'success': True, 'message': 'Order created'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        if 'user_id' in request.data:
            order.user = request.data.get('user_id')
        if 'shop_id' in request.data:
            order.shop = request.data.get('shop_id')
        if 'item_id' in request.data:
            order.item = request.data.get('item_id')
        if 'time' in request.data:
            order.time = request.data.get('time')
        if 'status' in request.data:
            order.status = request.data.get('status')

        order.save()

        return Response({'success': True, 'message': 'Order updated successfully'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'success': False, 'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response({'success': True, 'message': 'Order deleted successfully'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'success': False, 'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_orders(request, user_id):
    try:
        orders = Order.objects.filter(user=user_id)
        orders_data = OrderSerializer(orders, many=True).data
        return Response({'success': True, 'message': 'User orders fetched successfully', 'data': orders_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_shop_orders(request, shop_id):
    try:
        orders = Order.objects.filter(shop=shop_id)
        orders_data = OrderSerializer(orders, many=True).data
        return Response({'success': True, 'message': 'Shop orders fetched successfully', 'data': orders_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
