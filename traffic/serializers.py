from rest_framework import serializers

from traffic.models import RoadSegment, TrafficRecorder


class RoadSegmentSerializer(serializers.ModelSerializer):
    traffic_records_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoadSegment
        fields = "__all__"
        read_only_fields = ("traffic_records_count",)


class TrafficRecorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficRecorder
        fields = "__all__"
