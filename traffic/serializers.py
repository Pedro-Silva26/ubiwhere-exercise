from rest_framework import serializers

from traffic.models import RoadSegment, TrafficRecorder


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
