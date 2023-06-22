from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Review
from ..serializers import ReviewSerializer

@api_view(['POST'])
def create_review(request):
    """
    Create a new review.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the review data and status.

    Raises:
        Exception: If any error occurs during the review creation.

    """
    data = request.data
    required_fields = ['content', 'star', 'item', 'author']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        review = Review(**data)
        review.save()
        serializer = ReviewSerializer(review)
        return Response({'success': True, 'message': 'Review created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_reviews(request):
    """
    Get all reviews.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the reviews data and status.

    Raises:
        Exception: If any error occurs while retrieving the reviews.

    """
    try:
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'success': True, 'message': 'Reviews retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_review(request, id):
    """
    Get a specific review by ID.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the review.

    Returns:
        Response: The HTTP response containing the review data and status.

    Raises:
        Review.DoesNotExist: If the requested review does not exist.
        Exception: If any error occurs while retrieving the review.

    """
    try:
        review = Review.objects.get(id=id)
        serializer = ReviewSerializer(review)
        return Response({'success': True, 'message': 'Review retrieved successfully', 'data': serializer.data})
    except Review.DoesNotExist:
        return Response({'success': False, 'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_review(request, id):
    """
    Update a review by ID.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the review.

    Returns:
        Response: The HTTP response containing the updated review data and status.

    Raises:
        Review.DoesNotExist: If the requested review does not exist.
        Exception: If any error occurs while updating the review.

    """
    data = request.data
    required_fields = ['title', 'content']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        review = Review.objects.get(id=id)
        review.title = data['title']
        review.content = data['content']
        review.save()
        serializer = ReviewSerializer(review)
        return Response({'success': True, 'message': 'Review updated successfully', 'data': serializer.data})
    except Review.DoesNotExist:
        return Response({'success': False, 'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_review(request, id):
    """
    Delete a review by ID.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the review.

    Returns:
        Response: The HTTP response containing the status of the deletion.

    Raises:
        Review.DoesNotExist: If the requested review does not exist.
        Exception: If any error occurs while deleting the review.

    """
    try:
        review = Review.objects.get(id=id)
        review.delete()
        return Response({'success': True, 'message': 'Review deleted successfully'})
    except Review.DoesNotExist:
        return Response({'success': False, 'message': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
def get_review_of_an_item(request, item_id):
    """
    Get reviews of a specific item.

    Args:
        request (HttpRequest): The HTTP request object.
        item_id (int): The ID of the item.

    Returns:
        Response: The HTTP response containing the reviews data and status.

    Raises:
        Exception: If any error occurs while retrieving the reviews.

    """
    try: 
        reviews = Review.objects.filter(item=item_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'success': True, 'message': 'Reviews retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)