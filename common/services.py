from app1.models import create_user
from django.db import transaction

def sign_up_user(name, email, password):
    with transaction.atomic():
        user = create_user(name=name, email=email, password=password)