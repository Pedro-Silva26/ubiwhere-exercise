from datetime import datetime
from decimal import Decimal
from typing import List, Tuple

import pytest
from django.contrib.gis.geos import LineString
from faker import Faker

from sensors.models import Sensor
from traffic.models import RoadSegment, TrafficRecorder, TrafficCarRecord
from vehicles.models import Car


@pytest.fixture
def road_segment_factory(faker: Faker):
    created_objects = []

    def create_road_segment(
            name: str | None = None,
            coords: List[Tuple[Decimal, Decimal]] | None = None,
    ):
        if name is None:
            name = faker.street_name()
        if coords is None:
            coords = [faker.latlng() for _ in range(2)]

        road_segment = RoadSegment.objects.create(name=name, road=LineString(coords))
        created_objects.append(road_segment)
        return road_segment

    yield create_road_segment

    for obj in created_objects:
        obj.delete()


@pytest.fixture
def traffic_recorder_factory(road_segment_factory, faker: Faker):
    created_objects = []

    def create_traffic_recorder(road_segment: RoadSegment | None = None,
                                avg_speed: int | None = None, ):
        if road_segment is None:
            road_segment = road_segment_factory()
        if avg_speed is None:
            avg_speed = faker.pyfloat(min_value=0, max_value=100)
        traffic_recorder = TrafficRecorder.objects.create(road_segment=road_segment,
                                                          avg_speed=avg_speed)
        created_objects.append(traffic_recorder)
        return traffic_recorder

    yield create_traffic_recorder

    for obj in created_objects:
        obj.delete()


@pytest.fixture
def traffic_car_record_factory(road_segment_factory, car_factory, sensor_factory, faker: Faker, ):
    created_objects = []

    def create_traffic_car_record(
            road_segment: RoadSegment | None = None,
            car: Car | None = None,
            sensor: Sensor | None = None,
            timestamp: datetime | None = None,
    ):
        if road_segment is None:
            road_segment = road_segment_factory()

        if car is None:
            car = car_factory()
        if sensor is None:
            sensor = sensor_factory()
        if timestamp is None:
            timestamp = faker.date_time

        traffic_car_record = TrafficCarRecord.objects.create(road_segment=road_segment,
                                                             car=car,
                                                             sensor=sensor,
                                                             timestamp=timestamp)
        created_objects.append(traffic_car_record)
        return traffic_car_record

    yield create_traffic_car_record

    for obj in created_objects:
        obj.delete()
