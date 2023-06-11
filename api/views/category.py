from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from ..serializers import CategorySerializer

@api_view(['POST'])
def create_category(request):
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
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'success': True, 'message': 'Categories retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_category(request, id):
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
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return Response({'success': True, 'message': 'Category deleted successfully'})
    except Category.DoesNotExist:
        return Response({'success': False, 'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
