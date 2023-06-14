from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Order, User, Shop, Item
from ..serializers import OrderSerializer
from datetime import datetime


@api_view(['POST'])
def create_order(request):
    try:
        user_id = request.data.get('user_id')
        items = request.data.get('items')
        time = datetime.now().isoformat(timespec='seconds')
        status = request.data.get('status')
        address = request.data.get('address')
        total = request.data.get('total')

        # Retrieve the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User not found'}, status=404)

        # Group items by shop ID
        items_by_shop = {}
        for item in items:
            item_id = item.get('id')
            item_quantity = item.get('quantity')
            try:
                item = Item.objects.get(id=item_id)
                if item.quantity < item_quantity:
                    return Response({'success': False, 'message': 'Item is not enough'}, status=400)
            except Item.DoesNotExist:
                return Response({'success': False, 'message': 'Item not found'}, status=404)
        for item in items:
            item_quantity = item.get('quantity')
            item_shop_id = item.get('shop_id')
            try:
                shop = Shop.objects.get(id=item_shop_id)
            except Shop.DoesNotExist:
                return Response({'success': False, 'message': 'Shop not found'}, status=404)

            if item_shop_id not in items_by_shop:
                items_by_shop[item_shop_id] = []
            items_by_shop[item_shop_id].append(item)

        orders = []
        for shop_id, shop_items in items_by_shop.items():
            shop = Shop.objects.get(id=shop_id)
            order = Order(user=user, shop=shop, items=shop_items, time=time, status=status, address=address, total=total)
            order.save()
            orders.append(order)
            for item in shop_items:
                item_id = item.get('id')
                item_quantity = item.get('quantity')
                item = Item.objects.get(id=item_id)
                item.quantity -= item_quantity
                item.save()
        order_data = OrderSerializer(orders, many=True).data
        return Response({'success': True, 'message': 'Orders created', 'data': order_data}, status=201)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)

@api_view(['PUT'])
def update_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        if 'user_id' in request.data:
            order.user = request.data.get('user_id')
        if 'shop_id' in request.data:
            order.shop = request.data.get('shop_id')
        if 'items' in request.data:  # Updated field name to 'items'
            order.items = request.data.get('items')  # Updated field name to 'items'
        if 'time' in request.data:
            order.time = request.data.get('time')
        if 'status' in request.data:
            order.status = request.data.get('status')
        if 'address' in request.data:
            order.address = request.data.get('address')
        if 'total' in request.data:
            order.total = request.data.get('total')
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
def get_user_orders(request, id):
    try:
        user = User.objects.get(id=id)
        orders = Order.objects.filter(user=user)
        
        if not orders:
            return Response({'success': False, 'message': 'No orders found for the user.'}, status=status.HTTP_404_NOT_FOUND)
        
        orders_data = OrderSerializer(orders, many=True).data
        return Response({'success': True, 'message': 'User orders fetched successfully', 'data': orders_data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def get_shop_orders(request, id):
    try:
        shop = Shop.objects.get(id=id)
        orders = Order.objects.filter(shop=id)
        orders_data = OrderSerializer(orders, many=True).data
        return Response({'success': True, 'message': 'Shop orders fetched successfully', 'data': orders_data}, status=status.HTTP_200_OK)
    except Shop.DoesNotExist:
        return Response({'success': False, 'message': 'Shop not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
