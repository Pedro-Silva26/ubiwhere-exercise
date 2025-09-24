import django_filters
from django.db.models import QuerySet, OuterRef, Subquery, Case, When, Value, CharField

from django_project import settings
from traffic.models import RoadSegment, TrafficRecorder


class RoadSegmentsFilter(django_filters.FilterSet):
    traffic_intensity = django_filters.ChoiceFilter(
        choices=(
            ("Baixa", "Baixa"),
            ("Media", "Media"),
            ("Elevada", "Elevada"),
        ),
        method="filter_by_latest_intensity",
    )

    class Meta:
        model = RoadSegment
        fields = []

    @staticmethod
    def filter_by_latest_intensity(
            queryset: QuerySet[RoadSegment], name: str, value: str
    ) -> QuerySet[RoadSegment]:
        latest_avg_speed_subquery = (
            TrafficRecorder.objects.filter(road_segment=OuterRef("pk"))
            .order_by("-updated_at")
            .values("avg_speed")[:1]
        )

        queryset = queryset.annotate(
            latest_avg_speed=Subquery(latest_avg_speed_subquery),
            latest_intensity=Case(
                When(
                    latest_avg_speed__lte=settings.HIGH_INTENSITY_VALUE,
                    then=Value("Elevada"),
                ),
                When(
                    latest_avg_speed__lte=settings.MEDIUM_INTENSITY_VALUE,
                    then=Value("Media"),
                ),
                default=Value("Baixa"),
                output_field=CharField(),
            ),
        )

        return queryset.filter(latest_intensity=value)
