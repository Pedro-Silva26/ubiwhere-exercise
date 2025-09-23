from django.db import models

from core.models import TimeStampMixin


class Car(TimeStampMixin):
    license_plate = models.CharField(max_length=20, unique=True)
