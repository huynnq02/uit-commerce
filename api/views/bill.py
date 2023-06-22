from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Bill
from ..serializers import BillSerializer

@api_view(['POST'])
def create_bill(request):
    """
    Create a new bill.

    Args:
        request (HttpRequest): The HTTP request object containing the bill data.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Exception: If any error occurs while creating the bill.

    """
    data = request.data
    required_fields = ['amount', 'description']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        bill = Bill(**data)
        bill.save()
        serializer = BillSerializer(bill)
        return Response({'success': True, 'message': 'Bill created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_bills(request):
    """
    Retrieve all bills.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the retrieved bills.

    Raises:
        Exception: If any error occurs while retrieving the bills.

    """
    try:
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response({'success': True, 'message': 'Bills retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_bill(request, id):
    """
    Retrieve a specific bill by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the bill to retrieve.

    Returns:
        Response: The HTTP response containing the retrieved bill.

    Raises:
        Bill.DoesNotExist: If the bill with the specified ID does not exist.
        Exception: If any error occurs while retrieving the bill.

    """
    try:
        bill = Bill.objects.get(id=id)
        serializer = BillSerializer(bill)
        return Response({'success': True, 'message': 'Bill retrieved successfully', 'data': serializer.data})
    except Bill.DoesNotExist:
        return Response({'success': False, 'message': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_bill(request, id):
    """
    Update a specific bill.

    Args:
        request (HttpRequest): The HTTP request object containing the updated bill data.
        id (int): The ID of the bill to update.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Bill.DoesNotExist: If the bill with the specified ID does not exist.
        Exception: If any error occurs while updating the bill.

    """
    data = request.data
    required_fields = ['amount', 'description']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        bill = Bill.objects.get(id=id)
        bill.amount = data['amount']
        bill.description = data['description']
        bill.save()
        serializer = BillSerializer(bill)
        return Response({'success': True, 'message': 'Bill updated successfully', 'data': serializer.data})
    except Bill.DoesNotExist:
        return Response({'success': False, 'message': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_bill(request, id):
    """
    Delete a specific bill.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the bill to delete.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Bill.DoesNotExist: If the bill with the specified ID does not exist.
        Exception: If any error occurs while deleting the bill.

    """
    try:
        bill = Bill.objects.get(id=id)
        bill.delete()
        return Response({'success': True, 'message': 'Bill deleted successfully'})
    except Bill.DoesNotExist:
        return Response({'success': False, 'message': 'Bill not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
