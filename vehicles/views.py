from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from vehicles.models import Car
from vehicles.serializers import CarTrafficSerializer


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
