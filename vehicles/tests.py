from datetime import datetime, UTC, timedelta

import pytest
from faker import Faker
from rest_framework.test import APIClient

from traffic.fixtures import traffic_car_record_factory, road_segment_factory
from vehicles.fixtures import car_factory
from sensors.fixtures import sensor_factory


@pytest.mark.parametrize(("expected_response", "last_24_hour_timestamp"),
                         [(200, 12),
                          (200, 3), ])
@pytest.mark.django_db
def test_get_car_last_24_hours(traffic_car_record_factory, faker: Faker, expected_response, last_24_hour_timestamp,
                               car_factory, road_segment_factory, sensor_factory):
    """
    Test the endpoint for retrieving the vehicle's data for the last 24 hours.

    This test evaluates if the API correctly retrieves only those traffic car records within the
    last 24 hours from the current timestamp for a specific car, and ensures the accuracy of the
    response/status code.

    """
    def generate_timestamp_last(now: datetime, one_day_ago: datetime) -> datetime:
        return faker.date_time_between(start_date=one_day_ago, end_date=now, tzinfo=UTC)

    now = datetime.now(UTC)

    one_day_ago = now - timedelta(days=1)
    client = APIClient()
    car = car_factory(license_plate="test")
    for _ in range(last_24_hour_timestamp):
        traffic_car_record_factory(car=car, timestamp=generate_timestamp_last(now, one_day_ago))

    for _ in range(20):
        traffic_car_record_factory(car=car, timestamp=faker.date_time(end_datetime=one_day_ago, tzinfo=UTC))
    response = client.get(f"/api/vehicles/cars/{car.license_plate}")
    assert response.status_code == expected_response
