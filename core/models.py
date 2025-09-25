import uuid

from django.db import models


class TimeStampMixin(models.Model):
    """
    Mixin that provides timestamp fields to track creation and modification times.

    Attributes:
        created_at: DateTimeField automatically set to the current timestamp when the
            object is created.
        updated_at: DateTimeField automatically updated to the current timestamp whenever
            the object is saved.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SensorTokenAuth(models.Model):
    client = models.CharField(max_length=255, null=False)
    token = models.UUIDField(primary_key=True, null=False)
    is_active = models.BooleanField(default=True)
