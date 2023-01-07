from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from common.utils import validate_credentials

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    """
    Signup Serializer for user.
    .param username: Name of the user.
    .param email: Signup email of the user.
    .param password: User password.
    """

    name = serializers.CharField(max_length=64)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=6, max_length=64
    )

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise Exception("Sorry, Email/Username Already in Use")
        except User.DoesNotExist:
            return email

class SignInSerializer(serializers.Serializer):

    """
    SignIn Serializer for user.
    .param email: Signup email of the user.
    .param password: User password.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=6, max_length=64, validators=[validate_password]
    )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data['email']
        password = validated_data['password']
        validate_credentials(email, password)
        return validated_data
