from django.contrib.gis.db import models as gis
from core.models import TimeStampMixin
from django.db import models

from django_project import settings


class RoadSegment(models.Model):
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
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    avg_speed = models.FloatField()

    @property
    def intensity(self) -> str:
        if self.avg_speed <= settings.HIGH_INTENSITY_VALUE:
            return "Elevada"
        elif self.avg_speed <= settings.MEDIUM_INTENSITY_VALUE:
            return "Media"
        return "Baixa"

    class Meta:
        get_latest_by = "updated_at"
