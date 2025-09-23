import os

import pandas as pd
from django.core.management.base import BaseCommand

from sensors.models import Sensor


class Command(BaseCommand):
    """
    Provides a management command for importing sensor data from a data source provided by Ubiwhere.

    This class is used to fetch, parse, and store sensor information into the database.

    """

    help = "Import sensors.csv from given URL"

    def handle(self, *args, **options):
        csv_url = os.getenv("SENSOR_DATA_URL",
                            "https://raw.githubusercontent.com/Ubiwhere/Traffic-Speed/refs/heads/master/sensors.csv")

        try:
            df = pd.read_csv(csv_url)
        except Exception as e:
            self.stderr.write(f"Error loading CSV: {e}")
            return

        for index, row in df.iterrows():
            Sensor.objects.get_or_create(id=row["uuid"], name=row["name"])

        self.stdout.write(self.style.SUCCESS("CSV import completed."))
