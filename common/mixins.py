"""
mixins.py
Contain mixins for the project.
"""

# Local Imports
from django.db.models import (
    DateTimeField, 
    Model, 
    UUIDField
)

class AuditMixin(Model):
    created_at = DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = DateTimeField(auto_now=True, editable=False, null=True)
    created_by = UUIDField(null=True)
    updated_by = UUIDField(null=True)
    deleted_by = UUIDField(null=True)

    class Meta:
        abstract = True