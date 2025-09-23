from rest_framework import viewsets

from traffic.models import RoadSegment, TrafficRecorder
from traffic.serializers import RoadSegmentSerializer, TrafficRecorderSerializer


class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer


class TrafficRecorderViewSet(viewsets.ModelViewSet):
    queryset = TrafficRecorder.objects.all()
    serializer_class = TrafficRecorderSerializer
