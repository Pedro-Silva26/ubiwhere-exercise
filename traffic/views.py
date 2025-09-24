from rest_framework import viewsets

from traffic.filters import RoadSegmentsFilter
from traffic.models import RoadSegment, TrafficRecorder
from traffic.serializers import RoadSegmentSerializer, TrafficRecorderSerializer
from django_filters import rest_framework as filters


class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoadSegmentsFilter


class TrafficRecorderViewSet(viewsets.ModelViewSet):
    queryset = TrafficRecorder.objects.all()
    serializer_class = TrafficRecorderSerializer
