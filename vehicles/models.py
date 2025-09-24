from datetime import datetime, UTC, timedelta

from django.db import models

from core.models import TimeStampMixin


class Car(TimeStampMixin):
    """
    Represents a car with a specific license_plate

    This model is used to store and manage data related to a car,
    including its license plate and associated passage records. It
    includes features for querying passages related to the car within
    a specific time frame, such as the last 24 hours.
    Attributes:
      license_plate: Reference to unique car identifier.

    Methods:
      last_24_hours_passages
        Provides a function that returns the traffic car record instances on the last 24 hours
    """
    license_plate = models.CharField(max_length=20, unique=True)

    def last_24_hours_passages(self):
        since = datetime.now(UTC) - timedelta(days=1)
        return self.trafficcarrecord_set.filter(updated_at__gte=since)
