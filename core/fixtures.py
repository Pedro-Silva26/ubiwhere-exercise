import uuid

import pytest
from django.contrib.auth.models import User

from core.models import SensorTokenAuth


@pytest.fixture
def admin_user():
    """
    Create and return an admin user.
    """
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="password123",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def sensor_token():
    return SensorTokenAuth.objects.create(token=uuid.uuid4(), client="Test")
