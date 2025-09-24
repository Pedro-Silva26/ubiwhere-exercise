from django.urls import path, include
from rest_framework.routers import DefaultRouter

from traffic.views import RoadSegmentViewSet, TrafficRecorderViewSet, TrafficDataView

router = DefaultRouter()
router.register(r"road-segments", RoadSegmentViewSet)
router.register(r"traffic-records", TrafficRecorderViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("traffic-car-records/", TrafficDataView.as_view(), name="traffic-car-records"),
]
