from django.shortcuts import render
from uuid import uuid4

# Create your views here.
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from app1.serializer import (
    SignUpSerializer,
    SignInSerializer
)
from common.services import sign_up_user

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
        return Response("User Signed In successfuly!")