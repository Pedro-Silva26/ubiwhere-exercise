from django.core.management import BaseCommand
from django.contrib.auth.models import User

from core.models import SensorTokenAuth
from django_project import settings


class Command(BaseCommand):
    help = "Create a user and a sensor api token"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_user(
                username="admin",
                email="admin@example.com",
                password="123",
                is_staff=True,
                is_superuser=True,
            )

        if not SensorTokenAuth.objects.filter(client="ubiwhere").exists():
            token, _ = SensorTokenAuth.objects.get_or_create(client="ubiwhere", token=settings.DEFAULT_API_KEY)

        self.stdout.write(self.style.SUCCESS("Admin user and sensor token created."))
