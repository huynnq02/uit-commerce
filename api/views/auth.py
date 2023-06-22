from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from ..serializers import UserSerializer
import cloudinary
import cloudinary.uploader
from ..models import User
from ..config import *
import bcrypt


@api_view(['POST'])
def create_user(request):
    """
    Create a new user.

    Required POST parameters:
    - email: The email of the user.
    - password: The password of the user.

    Returns:
    Response: The HTTP response indicating the success or failure of the operation.

    Raises:
    Exception: If any error occurs while creating the user.
    """
    try:
        email = request.data.get('email')
        print(email)
        if User.objects.filter(email=email).count() > 0:
            return Response({'success': False, 'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        password = request.data.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        request.data['password'] = hashed_password

        user = User(**request.data)
        user.save()

        return Response({'success': True, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_user(request, id):
    """
    Update an existing user.

    Required PUT parameters:
    - Any field(s) that need to be updated, except 'id'.
    - If the 'picture' field is provided, it will be uploaded to Cloudinary and the URL will be stored in 'profile_picture' field of the user.

    Returns:
    Response: The HTTP response indicating the success or failure of the operation.

    Raises:
    User.DoesNotExist: If the user with the specified ID does not exist.
    Exception: If any error occurs while updating the user.
    """
    try:
        user = User.objects.get(id=id)

        # Update the user fields based on the data provided in the request body
        for key, value in request.data.items():
            if key == 'id':
                continue
            if key == 'picture':
                # Upload the picture to Cloudinary and get the URL
                upload_result = cloudinary.uploader.upload(value)
                profile_picture_url = upload_result['secure_url']
                setattr(user, 'profile_picture', profile_picture_url)
            else:
                setattr(user, key, value)

        user.save()
        user_data = UserSerializer(user).data
        return Response({'success': True, 'message': 'User update successful', 'data': user_data}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    """
    Authenticate and login a user.

    Required POST parameters:
    - email: The email of the user.
    - password: The password of the user.

    Returns:
    Response: The HTTP response indicating the success or failure of the operation.

    Raises:
    User.DoesNotExist: If the user with the specified email does not exist.
    Exception: If any error occurs while authenticating and logging in the user.
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.get(email=email)
        is_match = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
        if is_match:
            user_data = UserSerializer(user).data
            # Password is correct, authentication successful
            return Response({'success': True, 'message': 'Login successful', 'data': user_data}, status=200)
        else:
            # Password is incorrect
            return Response({'success': False, 'message': 'Incorrect password'}, status=401)

    except User.DoesNotExist:
        # User not found
        return Response({'success': False, 'message': 'User not found'}, status=404)

    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=500)
