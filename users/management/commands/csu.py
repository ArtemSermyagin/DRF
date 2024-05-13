from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(
            email='r@r.ru',
            username='r',
            password='1234',
            is_superuser=True,
            is_staff=True,
        )
