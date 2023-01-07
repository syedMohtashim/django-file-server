"""
models.py
Contains a Custom model for the app.
"""

# Standard Library Imports
from uuid import uuid4

# Local Imports
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from common.mixins import AuditMixin
from django.db.models import (
    CharField,
    EmailField,
    UUIDField,
)
from common.managers import UserManager
# Create your models here.

class User(AbstractBaseUser, AuditMixin):
    """
    A custom User model.
    """
    # Removed inherited fields
    username = None
    first_name = None
    last_name = None

    # Base model fields
    uuid = UUIDField(
        _("UUID"),
        default=uuid4,
        editable=False,
        help_text=_("A unique identifier for the user to be used internally."),
    )
    name = CharField(
        _("Name of the user"),
        max_length=64,
        help_text=_("The name of the user."),
    )
    email = EmailField(
        _("Email of the user"),
        max_length=64,
        unique=True,
        help_text=_("The email address of the user."),
    )
    password = CharField(
        _("Password of the user"),
        max_length=128,
        help_text=_("The hashed password of the user."),
    )

    # meta
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # user manager
    objects = UserManager()

def create_user(name, email, password):
    """
    Utility method to create a user
    :param name: Name of the user
    :param email: Email of the user
    :param password: Password of the user
    """
    user_id = uuid4()
    create_user_params = {
        "uuid": user_id,
        "name": name,
        "email": email,
        "created_by": user_id,
    }
    user = User.objects.create(**create_user_params)
    # Save the password's hash
    user.set_password(password)
    user.save()
    return user
