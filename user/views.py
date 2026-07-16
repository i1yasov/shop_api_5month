from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import ConfirmationCode
from .serializer import UserRegisterSerializer


class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code = str(random.randint(100000, 999999))
        ConfirmationCode.objects.create(user=user, code=code)
        return Response(
            {"user_id": user.id, "code": code}, status=status.HTTP_201_CREATED
        )


class AuthorizationAPIView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"key": token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ConfirmAPIView(APIView):

    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        confirmation = user.confirmation_code
        if confirmation.code == code:
            user.is_active = True
            user.save()
            return Response({"message": "User confirmed"})
        return Response({"error": "Wrong code"}, status=status.HTTP_400_BAD_REQUEST)
