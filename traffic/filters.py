import django_filters
from django.db.models import QuerySet, OuterRef, Subquery, Case, When, Value, CharField

from django_project import settings
from traffic.models import RoadSegment, TrafficRecorder


class RoadSegmentsFilter(django_filters.FilterSet):
    """
      FilterSet for filtering RoadSegment instances based on traffic intensity.

      This class defines a custom filter for road segments to be filtered
      based on the latest traffic intensity. The intensity is determined
      by analyzing the average speed of traffic recordings associated with
      each road segment and considering predefined intensity thresholds (Defined in settings).

      Attributes
      ----------
      traffic_intensity : ChoiceFilter
          A filter for selecting road segments based on traffic intensity
          ("Baixa", "Media", "Elevada").

      Methods
      -------
      filter_by_latest_intensity(queryset: QuerySet[RoadSegment], name: str, value: str) -> QuerySet[RoadSegment]
          Static method for filtering road segments by their latest traffic intensity.
      """

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
                When(latest_avg_speed__gt=settings.MEDIUM_INTENSITY_VALUE, then=Value("Baixa")),
                default=Value(None),
                output_field=CharField(),
            ),
        )

        return queryset.filter(latest_intensity=value)
