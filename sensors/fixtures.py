from uuid import UUID

import pytest
from faker import Faker

from sensors.models import Sensor


@pytest.fixture
def sensor_factory(faker: Faker):
    created_objects = []

    def create_sensor(
            name: str | None = None,
            sensor_id: UUID | None = None,
    ):
        if name is None:
            name = faker.name
        if sensor_id is None:
            sensor_id = faker.uuid4()
        sensor = Sensor.objects.create(name=name, id=sensor_id)
        created_objects.append(sensor)
        return sensor

    yield create_sensor

    for obj in created_objects:
        obj.delete()
