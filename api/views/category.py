from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from ..serializers import CategorySerializer

@api_view(['POST'])
def create_category(request):
    """
    Create a new category.

    Args:
        request (HttpRequest): The HTTP request object containing the category data.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Exception: If any error occurs while creating the category.

    """
    data = request.data
    required_fields = ['name']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category(**data)
        category.save()
        serializer = CategorySerializer(category)
        return Response({'success': True, 'message': 'Category created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_categories(request):
    """
    Retrieve all categories.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the retrieved categories.

    Raises:
        Exception: If any error occurs while retrieving the categories.

    """
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'success': True, 'message': 'Categories retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_category(request, id):
    """
    Retrieve a specific category by its ID.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the category to retrieve.

    Returns:
        Response: The HTTP response containing the retrieved category.

    Raises:
        Category.DoesNotExist: If the category with the specified ID does not exist.
        Exception: If any error occurs while retrieving the category.

    """
    try:
        category = Category.objects.get(id=id)
        serializer = CategorySerializer(category)
        return Response({'success': True, 'message': 'Category retrieved successfully', 'data': serializer.data})
    except Category.DoesNotExist:
        return Response({'success': False, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_category(request, id):
    """
    Update a specific category.

    Args:
        request (HttpRequest): The HTTP request object containing the updated category data.
        id (int): The ID of the category to update.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Category.DoesNotExist: If the category with the specified ID does not exist.
        Exception: If any error occurs while updating the category.

    """
    data = request.data
    required_fields = ['name']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=id)
        category.name = data['name']
        category.save()
        serializer = CategorySerializer(category)
        return Response({'success': True, 'message': 'Category updated successfully', 'data': serializer.data})
    except Category.DoesNotExist:
        return Response({'success': False, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_category(request, id):
    """
    Delete a specific category.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the category to delete.

    Returns:
        Response: The HTTP response indicating the success or failure of the operation.

    Raises:
        Category.DoesNotExist: If the category with the specified ID does not exist.
        Exception: If any error occurs while deleting the category.

    """
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return Response({'success': True, 'message': 'Category deleted successfully'})
    except Category.DoesNotExist:
        return Response({'success': False, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
