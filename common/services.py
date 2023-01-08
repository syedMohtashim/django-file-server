from app1.models import create_user
from django.db import transaction
from django.contrib.auth import get_user_model
from common.tokens import generate_auth_tokens


User = get_user_model()



def sign_up_user(name, email, password):
    with transaction.atomic():
        user = create_user(name=name, email=email, password=password)

def sign_in(email):
    """
    A utility function to sign-In a user.

    # Parameters
    ----------
    email: User's email.

    # Returns
    ----------
    response: A tuple of success and tokens.
    """
    user = User.objects.get(email=email)
    # TODO: Add 2FA.

    # If the user has disabled 2FA, and signin up:
    refresh_token, access_token = generate_auth_tokens(user)
    return (
            {
                "access": access_token,
                "refresh": refresh_token,
            },
            True,
        )
    