import os

import pandas as pd
from django.contrib.gis.geos import LineString
from django.core.management.base import BaseCommand

from traffic.models import RoadSegment, TrafficRecorder


class Command(BaseCommand):
    """
    Provides a management command for importing road segments and traffic recorder data from a data source provided by Ubiwhere.

    This class is used to fetch, parse, and store sensor information into the database.

    """

    help = "Import traffic_speed.csv from given URL"

    def handle(self, *args, **options):
        csv_url = os.getenv("TRAFFIC_DATA_URL",
                            "https://raw.githubusercontent.com/Ubiwhere/Traffic-Speed/master/traffic_speed.csv")

        try:
            df = pd.read_csv(csv_url)
        except Exception as e:
            self.stderr.write(f"Error loading CSV: {e}")
            return

        for index, row in df.iterrows():
            start = (row["Long_start"], row["Lat_start"])
            end = (row["Long_end"], row["Lat_end"])

            line = LineString(start, end)
            obj, created = RoadSegment.objects.get_or_create(road=line)
            TrafficRecorder.objects.get_or_create(
                road_segment=obj,
                avg_speed=row["Speed"],
            )

        self.stdout.write(self.style.SUCCESS("CSV import completed."))
