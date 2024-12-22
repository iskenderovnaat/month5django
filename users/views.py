from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode


@api_view(['POST'])
def confirm_user_api_view(request):
    username = request.data.get('username')
    code = request.data.get('code')

    try:
        user = User.objects.get(username=username)
        confirmation = ConfirmationCode.objects.get(user=user)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except ConfirmationCode.DoesNotExist:
        return Response({'error': 'Confirmation code not found'}, status=status.HTTP_404_NOT_FOUND)

    if confirmation.code == code:
        user.is_active = True
        user.save()
        print(f"User {user.username} is_active: {user.is_active}")
        confirmation.delete()
        return Response({'message': 'User confirmed successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password, is_active=False)


    code = ConfirmationCode.generate_code()
    ConfirmationCode.objects.create(user=user, code=code)

    return Response({'user_id': user.id, 'confirmation_code': code}, status=status.HTTP_201_CREATED)