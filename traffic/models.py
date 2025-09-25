from django.contrib.gis.db import models as gis
from core.models import TimeStampMixin
from django.db import models

from django_project import settings
from sensors.models import Sensor
from vehicles.models import Car


class RoadSegment(models.Model):
    """
      Represents a segment of a road with associated traffic data.

      This class models a segment of a road, including its name and spatial geometry.
      It provides mechanisms to access related traffic records and their details.
      Each road segment is defined by a unique LineString geometry.

      Attributes:
          name: The name of the road segment.
          road: A unique LineString geometry that represents the road segment.

      Methods
      -------
      traffic_records_count
          Provides a computed value indicating the number of times that been registered a traffic record
      latest_traffic_record_intensity
          Provides a computed value indicating the latest degree of intensity registered by traffic record

      """
    name = models.CharField(max_length=100)
    road = gis.LineStringField(
        unique=True,
    )

    @property
    def traffic_records_count(self):
        return self.trafficrecorder_set.count()

    @property
    def latest_traffic_record_intensity(self):
        return self.trafficrecorder_set.latest().intensity


class TrafficRecorder(TimeStampMixin):
    """
    Represents a traffic recorder for a specific road segment.

    The TrafficRecorder class serves as a model to store and manage traffic data for a road
    segment, including the average speed of vehicles. It provides a computed property to
    determine traffic intensity based on predefined thresholds.

    Attributes
    ----------
    road_segment : ForeignKey
        Reference to the associated road segment.
    avg_speed : Float
        Average speed of vehicles on the road segment.

    Methods
    -------
    intensity
        Provides a computed value indicating traffic intensity based on average speed predefined thresholds.

    Meta
    ----
    get_latest_by : str
        Defines the field used to determine the latest object in the model.
    """
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    avg_speed = models.FloatField()

    @property
    def intensity(self) -> str | None:
        if self.avg_speed <= settings.HIGH_INTENSITY_VALUE:
            return "Elevada"
        elif self.avg_speed <= settings.MEDIUM_INTENSITY_VALUE:
            return "Media"
        elif self.avg_speed > settings.MEDIUM_INTENSITY_VALUE:
            return "Baixa"
        return None

    class Meta:
        get_latest_by = "updated_at"


class TrafficCarRecord(models.Model):
    """
    Represents a record of car traffic for a specific road segment and sensor.

    This model captures information about a car's presence at a specific road segment
    detected by a sensor (Can be moving sensor) at a precise point in time. It is intended for use in traffic
    monitoring and analysis systems.

    Attributes:
        road_segment: Reference to the associated road segment.
        car: Reference to the associated car.
        sensor: Reference to the associated sensor.
        timestamp: The exact date and time when the sensor detected the car at the given
            road segment.
    """

    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
