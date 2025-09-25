from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import RetrieveAPIView

from core.serializers import ErrorSerializer
from vehicles.models import Car
from vehicles.serializers import CarTrafficSerializer

@extend_schema(responses={
    200: CarTrafficSerializer,
    401: ErrorSerializer,
    403: ErrorSerializer,
    404: ErrorSerializer,
})
class CarTrafficView(RetrieveAPIView):
    """
    Handles retrieval operations for car traffic data.

    This class-based view is responsible for retrieving specific car traffic
    information based on a unique license plate identifier. It provides
    an integration with TrafficCarRecord to retrieve historic passages data.

    Attributes:
        queryset: Queryset definition for retrieving all Car model records.
        serializer_class: Serializer class used for formatting the output data.
        lookup_field: Field used to look up specific Car model records (license_plate).
    """

    queryset = Car.objects.all()
    serializer_class = CarTrafficSerializer
    lookup_field = "license_plate"
