from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentication import SensorTokenAuthentication
from core.permissions import SensorTokenAuthPermission
from core.serializers import ErrorSerializer
from traffic.filters import RoadSegmentsFilter
from traffic.models import RoadSegment, TrafficRecorder, TrafficCarRecord
from traffic.serializers import RoadSegmentSerializer, TrafficRecorderSerializer, TrafficRecordListSerializer, \
    TrafficRecordSerializer
from django_filters import rest_framework as filters


@extend_schema_view(
    list=extend_schema(
        responses={200: RoadSegmentSerializer(many=True)},
    ),
    retrieve=extend_schema(
        responses={
            200: RoadSegmentSerializer,
            404: ErrorSerializer,
        }
    ),
    create=extend_schema(
        responses={
            201: RoadSegmentSerializer,
            400: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,

        }
    )
    ,
    update=extend_schema(
        responses={
            200: RoadSegmentSerializer,
            400: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,
            404: ErrorSerializer,
        }
    )
    ,
    destroy=extend_schema(
        responses={
            204: RoadSegmentSerializer,
            401: ErrorSerializer,
            403: ErrorSerializer,
            404: ErrorSerializer,
        }
    )
    ,
    partial_update=extend_schema(
        responses={
            200: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,
            404: ErrorSerializer,
        }
    )
)
class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    Handles operations for road segment data management.

   This class enables CRUD (Create, Read, Update, Delete) operations
    on traffic data records. It requires basic authentication on protected methods (POST, PUT, PATCH).
    This viewset also supports filtering of a road segment by latest traffic intensity.
    It requires basic authentication on protected methods (POST, PUT, PATCH).

    Attributes
    ----------
    queryset : QuerySet
        The queryset containing all RoadSegments objects. Defines the dataset
        the viewset operates on.
    serializer_class : RoadSegmentSerializer
        Specifies the serializer used to handle JSON serialization and
        deserialization of RoadSegment objects.
    filter_backends : tuple
        Specifies the filter backends used for filtering operations.
    filterset_class : RoadSegmentsFilter
        Specifies the filter class used for intensity filtering.
    """

    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoadSegmentsFilter


@extend_schema_view(
    list=extend_schema(
        responses={200: TrafficRecorderSerializer(many=True)},
    ),
    retrieve=extend_schema(
        responses={
            200: TrafficRecorderSerializer,
            404: ErrorSerializer,
        }
    ),
    create=extend_schema(
        responses={
            201: TrafficRecorderSerializer,
            400: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,

        }
    )
    ,
    update=extend_schema(
        responses={
            200: TrafficRecorderSerializer,
            400: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,
            404: ErrorSerializer,
        }
    )
    ,
    destroy=extend_schema(
        responses={
            204: TrafficRecorderSerializer,
            401: ErrorSerializer,
            403: ErrorSerializer,
            404: ErrorSerializer,
        }
    )
    ,
    partial_update=extend_schema(
        responses={
            200: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,
            404: ErrorSerializer,
        }
    )
)
class TrafficRecorderViewSet(viewsets.ModelViewSet):
    """
    Handles operations for recording and managing traffic data.

    This class enables CRUD (Create, Read, Update, Delete) operations
    on traffic data records. It requires basic authentication on protected methods (POST, PUT, PATCH).

    Attributes
    ----------
    queryset : QuerySet
        The queryset containing all TrafficRecorder objects. Defines the dataset
        the viewset operates on.
    serializer_class : TrafficRecordListSerializer
        Specifies the serializer used to handle JSON serialization and
        deserialization of TrafficRecorder objects.
    """
    queryset = TrafficRecorder.objects.all()
    serializer_class = TrafficRecorderSerializer


class TrafficDataView(APIView):
    queryset = TrafficCarRecord.objects.all()
    serializer_class = TrafficRecordListSerializer
    permission_classes = [SensorTokenAuthPermission]
    authentication_classes = [SensorTokenAuthentication]

    @extend_schema(
        responses={
            201: TrafficRecordSerializer(many=True),
            400: OpenApiResponse(),
            401: ErrorSerializer,
            403: ErrorSerializer,
        }
    )
    def post(self, request):
        """
        Handles POST requests to create multiple traffic records.

        This method processes a POST request containing multiple traffic records data,
        validates the data using a serializer, and saves the records if the data is valid.
        If the data fails validation, it returns the errors with a bad request status.
        It requires a api-key in the request header.

        Raises:
            ValidationError: If the provided data is invalid.

        Args:
            request: The HTTP request object containing the payload with traffic records.

        Returns:
            Response: The HTTP response with a success message and the number of records
            created, or an error message with a status code of 400 if the data is invalid.
        """
        serializer = TrafficRecordSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "records_created": len(serializer.validated_data)}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
