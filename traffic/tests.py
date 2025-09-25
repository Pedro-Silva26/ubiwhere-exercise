import random
import uuid

from faker import Faker
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from django_project import settings
from traffic.fixtures import traffic_recorder_factory, road_segment_factory
from vehicles.fixtures import car_factory
from sensors.fixtures import sensor_factory
from core.fixtures import sensor_token

PROTECTED_ENDPOINTS = [
    ("post", "/api/traffic/road-segments/"),
    ("put", "/api/traffic/road-segments/"),
    ("delete", "/api/traffic/road-segments/"),
    ("patch", "/api/traffic/road-segments/"),
    ("post", "/api/traffic/traffic-records/"),
    ("put", "/api/traffic/traffic-records/"),
    ("delete", "/api/traffic/traffic-records/"),
    ("patch", "/api/traffic/traffic-records/"),
]


@pytest.mark.parametrize(("method", "url"), PROTECTED_ENDPOINTS)
@pytest.mark.django_db
def test_unauthenticated_protected_endpoints(method: str, url: str):
    """
    Test endpoints protected for unauthenticated users.
    """
    client = APIClient()
    response = getattr(client, method)(url)
    assert (
            response.status_code == 401
    ), f"{method.upper()} {url} returned {response.status_code}, expected 401"


@pytest.mark.parametrize(("method", "url"), PROTECTED_ENDPOINTS)
@pytest.mark.django_db
def test_authenticated_protected_endpoints(method: str, url: str, admin_user: User):
    """
    Test endpoints unprotected for unauthenticated users.
    """
    client = APIClient()
    client.force_authenticate(admin_user)
    response = getattr(client, method)(url)
    assert (
            response.status_code != 401
    ), f"{method.upper()} {url} returned {response.status_code}, expected != 401"


@pytest.mark.parametrize(("filter", "expected_output"), [("Baixa", 4), ("Media", 5), ("Elevada", 6)])
@pytest.mark.django_db
def test_road_segment_filter(filter: str, expected_output: int, traffic_recorder_factory, road_segment_factory):
    """
    Test the filtering of road segments based on their traffic intensity levels.

    This function uses parameterized test cases to validate if filtering road segments by traffic
    intensity (Low, Medium, High) returns the correct expected output. The test involves traffic
    records with average speed values that correspond to the specific intensity filter.

    """

    def get_intensity_value(filter_designation: str):
        MAX_VALUE_AVG_SPEED = 300
        values = {"Elevada": random.randint(0, settings.HIGH_INTENSITY_VALUE),
                  "Media": random.randint(settings.HIGH_INTENSITY_VALUE + 1, settings.MEDIUM_INTENSITY_VALUE),
                  "Baixa": random.randint(settings.MEDIUM_INTENSITY_VALUE + 1, MAX_VALUE_AVG_SPEED), }
        return values[filter_designation]

    intensity = ["Baixa", "Media", "Elevada"]
    intensity.remove(filter)
    client = APIClient()
    expected_response = []
    for _ in range(expected_output):
        road_segment = road_segment_factory()
        expected_response.append(road_segment)
        for _ in range(random.randint(1, 4)):
            traffic_recorder_factory(road_segment=road_segment)
        traffic_recorder_factory(road_segment=road_segment, avg_speed=get_intensity_value(filter))

    for _ in range(random.randint(1, 20)):
        road_segment = road_segment_factory()
        for _ in range(random.randint(1, 4)):
            traffic_recorder_factory(road_segment=road_segment)
        traffic_recorder_factory(road_segment=road_segment, avg_speed=get_intensity_value(random.choice(intensity)))

    response = client.get(f"/api/traffic/road-segments/?traffic_intensity={filter}")
    returned_ids = [rs["id"] for rs in response.data["results"]]
    assert set(returned_ids) == set([rs.id for rs in expected_response])


@pytest.mark.parametrize(("create_car", "sensor_exist", "is_auth", "expected_response", "last_24_hour_timestamp"),
                         [(True, True, False, 403, 12),
                          (True, False, True, 400, 3),
                          (False, True, True, 200, 4), ])
@pytest.mark.django_db
def test_create_car_records(sensor_factory, road_segment_factory, car_factory, sensor_exist, create_car,
                            expected_response, last_24_hour_timestamp, faker: Faker, is_auth, sensor_token):
    """
    Test case for creating car records.

    This test case checks the functionality of creating car records with various
    combinations of car and sensor existence, user authentication, and expected
    responses. It simulates different scenarios using parameterized inputs, creates
    or skips the creation of cars and sensors accordingly (Sensors must be already in database), and tests the endpoint
    for creating traffic car records.

    """
    client = APIClient()
    sensor_uuid = uuid.uuid4()
    data = []
    api_key = None
    if is_auth:
        api_key = sensor_token.token
    if sensor_exist:
        sensor = sensor_factory()
        sensor_uuid = sensor.id

    car_license_plate = faker.license_plate()
    if create_car:
        car = car_factory()
        car_license_plate = car.license_plate

    for _ in range(last_24_hour_timestamp):
        road_segment = road_segment_factory()
        data.append({"road_segment": road_segment.id,
                     "car__license_plate": car_license_plate,
                     "timestamp": faker.date_time(),
                     "sensor__uuid": sensor_uuid, })
    response = client.post(f"/api/traffic/traffic-car-records/", data, format="json", headers={'api-key': api_key})
    assert response.status_code == expected_response
