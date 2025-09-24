from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from traffic.filters import RoadSegmentsFilter
from traffic.models import RoadSegment, TrafficRecorder, TrafficCarRecord
from traffic.serializers import RoadSegmentSerializer, TrafficRecorderSerializer, TrafficRecordListSerializer, \
    TrafficRecordSerializer
from django_filters import rest_framework as filters


class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoadSegmentsFilter


class TrafficRecorderViewSet(viewsets.ModelViewSet):
    queryset = TrafficRecorder.objects.all()
    serializer_class = TrafficRecorderSerializer


class TrafficDataView(APIView):
    queryset = TrafficCarRecord.objects.all()
    serializer_class = TrafficRecordListSerializer

    def post(self, request):
        serializer = TrafficRecordSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "records_created": len(serializer.validated_data)}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
