from rest_framework import serializers

from sensors.models import Sensor
from traffic.models import RoadSegment, TrafficRecorder, TrafficCarRecord
from vehicles.models import Car


class RoadSegmentSerializer(serializers.ModelSerializer):
    traffic_records_count = serializers.IntegerField(read_only=True)
    latest_traffic_record_intensity = serializers.CharField(read_only=True)

    class Meta:
        model = RoadSegment
        fields = "__all__"
        read_only_fields = ("traffic_records_count", "latest_traffic_record_intensity",)


class TrafficRecorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficRecorder
        fields = "__all__"


class TrafficRecordSerializer(serializers.Serializer):
    road_segment = serializers.IntegerField()
    car__license_plate = serializers.CharField(max_length=20)
    timestamp = serializers.DateTimeField()
    sensor__uuid = serializers.UUIDField()

    def create(self, validated_data):
        car, _ = Car.objects.get_or_create(
            license_plate=validated_data["car__license_plate"]
        )

        try:
            sensor = Sensor.objects.get(id=validated_data["sensor__uuid"])
        except Sensor.DoesNotExist:
            raise serializers.ValidationError("Sensor not registered.")

        try:
            road_segment = RoadSegment.objects.get(id=validated_data["road_segment"])
        except RoadSegment.DoesNotExist:
            raise serializers.ValidationError("Road Segment not registered.")

        return TrafficCarRecord.objects.create(
            car=car,
            road_segment=road_segment,
            timestamp=validated_data["timestamp"],
            sensor=sensor
        )


class TrafficRecordListSerializer(serializers.ListSerializer):
    child = TrafficRecordSerializer()

    def create(self, validated_data):
        records = [self.child.create(item) for item in validated_data]
        return records


class TrafficRecordDetailSerializer(serializers.ModelSerializer):
    sensor_uuid = serializers.UUIDField(source='sensor.id')
    sensor_name = serializers.CharField(source='sensor.name')
    road_segment = RoadSegmentSerializer()

    class Meta:
        model = TrafficCarRecord
        fields = ['road_segment', 'timestamp', 'sensor_uuid', 'sensor_name']