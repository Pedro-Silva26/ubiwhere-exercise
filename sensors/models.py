import uuid
from django.db import models


class Sensor(models.Model):
    """
    Represents a sensor with a unique identifier (uuid) and a name.

    Attributes:
        id: The unique identifier for the sensor. This is a UUIDField that serves as the
            primary key.
        name: The name of the sensor. This is a CharField with a maximum length of 150
            characters and cannot be null.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=False)
