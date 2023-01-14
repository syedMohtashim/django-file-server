from django.shortcuts import render
from uuid import uuid4

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from app1.serializer import (
    SignUpSerializer,
    SignInSerializer
)
from common.services import sign_up_user
from common.services import sign_in
from common.utils import TokenUtils

User = get_user_model()



class SignUpAPIView(APIView):
    """
    APIView for User SignUp.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data
        # create_user_params = {
        #     "username": validated_data['username'],
        #     "email": validated_data['email'],
        # }
        # user = User.objects.create(**create_user_params)
        sign_up_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        
        return Response("User Created Successfully")


class SignInAPIView(APIView):
    """
    APIView for user signin.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        request_data = request.data
        serializer = SignInSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        # Get the acces and refresh tokens along with a success( Ture | False ) Flag
        tokens, success = sign_in(validated_data['email'])

        # Set the response.
        response = Response(
            data={"success": success, "Message": "User Signed In successfuly!" },
            status=status.HTTP_200_OK,
        )

        # Set the tokens
        TokenUtils.set_cookie(response=response, tokens=tokens)

        return response

class SignOutAPIView(APIView):
    """
    APIView to signout an already signed-in user.
    """
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        # Get the refresh token from request
        refresh_token = request.COOKIES.get("refresh")

        # blacklist it
        RefreshToken(refresh_token).blacklist()

        # Set Response
        response = Response(
            data={"success": True, "Message": "User Signed Out successfuly!" },
            status=status.HTTP_200_OK,
        )

        # Clear the cookies
        TokenUtils.clear_cookies(response)

        # Return Response
        return response


class FileUploadAPIView(APIView):
    """
    APIView with which a logged in User can
    upload a file.
    """