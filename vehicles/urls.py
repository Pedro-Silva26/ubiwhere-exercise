from django.urls import path

from vehicles.views import CarTrafficView

urlpatterns = [
    path(r"cars/<str:license_plate>", CarTrafficView.as_view(), name="cars"),
]
