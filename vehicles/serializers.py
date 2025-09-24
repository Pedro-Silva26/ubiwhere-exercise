from datetime import datetime, UTC, timedelta

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from traffic.models import TrafficCarRecord
from traffic.serializers import TrafficRecordDetailSerializer
from vehicles.models import Car


class CarTrafficSerializer(serializers.ModelSerializer):
    """
    Serializer class for representing car traffic data.

    This class is used to serialize and deserialize data related to car traffic. It includes
    information about a car, such as its license plate, the time it was last updated, and details
    of its traffic records within the last 24 hours.

    Attributes:
        passages_last_24h: A nested serializer providing detailed information about
            traffic records associated with the car in the last 24 hours.

    Methods:
        get_passages_last_24h(obj):
            Retrieves and serializes traffic records for the car from the last 24 hours.

    """

    passages_last_24h = SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ["license_plate", "updated_at", "passages_last_24h"]

    @extend_schema_field(TrafficRecordDetailSerializer)
    def get_passages_last_24h(self, obj):
        since = datetime.now(UTC) - timedelta(days=1)
        records = TrafficCarRecord.objects.filter(car=obj, timestamp__gte=since)
        return TrafficRecordDetailSerializer(records, many=True).data
