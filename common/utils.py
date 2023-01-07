from django.contrib.auth import get_user_model

User = get_user_model()


def validate_credentials(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise Exception
    
    if not user.check_password(password):
        raise Exception

    if not user.is_active:
        raise Exception 