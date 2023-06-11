from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Report
from ..serializers import ReportSerializer

@api_view(['POST'])
def create_report(request):
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
    try:
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response({'success': True, 'message': 'Reports retrieved successfully', 'data': serializer.data})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_report(request, id):
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
    try:
        report = Report.objects.get(id=id)
        report.delete()
        return Response({'success': True, 'message': 'Report deleted successfully'})
    except Report.DoesNotExist:
        return Response({'success': False, 'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
