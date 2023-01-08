from django.contrib.auth import get_user_model
from datetime import datetime
from time import time
from django.conf import settings


User = get_user_model()

# TODO: Add custom exceptions.
def validate_credentials(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Exception
    
    if not user.check_password(password):
        raise Exception

    if not user.is_active:
        raise Exception


class TokenUtils:
    """
    Manages access and refresh tokens.
    """

    @classmethod
    def set_cookie(cls, response, tokens):
        """
        Sets access and refresh tokens in response.
        """
        access_token = tokens.get('access')
        refresh_cookie = tokens.get('refresh')

        # Set access and refresh Tokens in response
        cls._set_access_token_in_response(
            response=response, access_token=access_token
        )
        cls._set_refresh_token_in_response(
            response=response, refresh_token=refresh_cookie
        )

    @classmethod
    def _set_access_token_in_response(cls, response, access_token):
        """
        Sets access token in response.
        """
        # Calculate the expiry of access token.
        expiry = cls._get_token_expiry(lifetime=settings.ACCESS_TOKEN_LIFETIME)

        # set access token in the response
        cls._set_cookie_in_response(
            response=response,
            key="access",
            value=access_token,
            expiry=expiry,
            samesite= 'Lax',    # ACCESS_COOKIE_SAMESITE,
            domain=None,        # ACCESS_COOKIE_DOMAIN
            path="/",           # ACCESS_COOKIE_PATH
            secure=False,       # ACCESS_COOKIE_SECURE
        )

    @classmethod
    def _set_refresh_token_in_response(cls, response, refresh_token):
        """
        Sets refresh token in response.
        """
        # Calculate the expiry of access token.
        expiry = cls._get_token_expiry(lifetime=settings.REFRESH_TOKEN_LIFETIME)

        # set refresh token in the response
        cls._set_cookie_in_response(
            response=response,
            key="refresh",
            value=refresh_token,
            expiry=expiry,
            samesite= 'Lax',    # REFRESH_COOKIE_SAMESITE,
            domain=None,        # REFRESH_COOKIE_DOMAIN
            path="/",           # REFRESH_COOKIE_PATH
            secure=False,       # REFRESH_COOKIE_SECURE
        )

    @classmethod
    def _get_token_expiry(cls, lifetime):
        """
        Returns the expiry date time for a token.
        """
        # Get the current time
        curr_time = int(time())

        # Get the token expiry in UTC epoch
        expiry = curr_time + (
            lifetime.total_seconds() - settings.NETWORK_TOLERENCE
        )

        # convert into a time stamp
        expiry = datetime.fromtimestamp(int(expiry))

        return expiry

    @classmethod
    def _set_cookie_in_response(
        cls,
        response,
        key,
        value,
        expiry,
        samesite,
        domain,
        path,
        secure,
    ):
        """Sets the provided key value pair in response cookie"""
        response.set_cookie(
            key=key,
            value=value,
            max_age=None,
            expires=expiry,
            path=path,
            domain=domain,
            secure=secure,
            httponly=True,
            samesite=samesite,
        )
