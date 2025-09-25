import pytest
from faker import Faker

from vehicles.models import Car


@pytest.fixture
def car_factory(faker: Faker, ):
    created_objects = []

    def create_car(license_plate: str | None = None):
        if license_plate is None:
            license_plate = faker.license_plate()
        car = Car.objects.create(license_plate=license_plate)
        created_objects.append(car)
        return car

    yield create_car

    for obj in created_objects:
        obj.delete()
