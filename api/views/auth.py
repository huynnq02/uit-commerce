from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserSerializer
from ..models import User
from ..config import *
import bcrypt


@api_view(['POST'])
def create_user(request):
    email = request.data.get('email')
    print(email)
    if User.objects.filter(email=email).count() > 0:
        return Response({'success': False, 'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)
   
    password = request.data.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    request.data['password'] = hashed_password

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User(**serializer.validated_data)
        user.save()
        
        return Response({'success': True, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'success': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        if email and User.objects(email=email, id__ne=id).count() > 0:
            return Response({'success': False, 'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        serializer.save()
        return Response({'success': True, 'message': 'User updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'success': False, 'message': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        if is_match:
            # Password is correct, authentication successful
            return Response({'success': True, 'message': 'Login successful', 'data': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            # Password is incorrect
            return Response({'success': False, 'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        # User not found
        return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

   

