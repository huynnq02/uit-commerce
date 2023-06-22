from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Report
from ..serializers import ReportSerializer

@api_view(['POST'])
def create_report(request):
    """
    Create a new report.

    Args:
        request (HttpRequest): The HTTP request object containing the report data.

    Returns:
        Response: The HTTP response containing the created report data.

    Raises:
        Exception: If any error occurs while creating the report.

    """
    data = request.data
    required_fields = ['title', 'description']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        report = Report(**data)
        report.save()
        serializer = ReportSerializer(report)
        return Response({'success': True, 'message': 'Report created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_reports(request):
    """
    Retrieve all reports.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response containing the retrieved reports data.

    Raises:
        Exception: If any error occurs while retrieving the reports.

    """
    try:
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response({'success': True, 'message': 'Reports retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_report(request, id):
    """
    Retrieve a specific report.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the report.

    Returns:
        Response: The HTTP response containing the retrieved report data.

    Raises:
        Report.DoesNotExist: If the report with the specified ID does not exist.
        Exception: If any error occurs while retrieving the report.

    """
    try:
        report = Report.objects.get(id=id)
        serializer = ReportSerializer(report)
        return Response({'success': True, 'message': 'Report retrieved successfully', 'data': serializer.data})
    except Report.DoesNotExist:
        return Response({'success': False, 'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_report(request, id):
    """
    Update a report.

    Args:
        request (HttpRequest): The HTTP request object containing the updated report data.
        id (int): The ID of the report.

    Returns:
        Response: The HTTP response containing the updated report data.

    Raises:
        Report.DoesNotExist: If the report with the specified ID does not exist.
        Exception: If any error occurs while updating the report.

    """
    data = request.data
    required_fields = ['title', 'description']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return Response({'success': False, 'message': f'Missing fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        report = Report.objects.get(id=id)
        report.title = data['title']
        report.description = data['description']
        report.save()
        serializer = ReportSerializer(report)
        return Response({'success': True, 'message': 'Report updated successfully', 'data': serializer.data})
    except Report.DoesNotExist:
        return Response({'success': False, 'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_report(request, id):
    """
    Delete a report.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the report.

    Returns:
        Response: The HTTP response indicating the success or failure of the delete operation.

    Raises:
        Report.DoesNotExist: If the report with the specified ID does not exist.
        Exception: If any error occurs while deleting the report.

    """
    try:
        report = Report.objects.get(id=id)
        report.delete()
        return Response({'success': True, 'message': 'Report deleted successfully'})
    except Report.DoesNotExist:
        return Response({'success': False, 'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
