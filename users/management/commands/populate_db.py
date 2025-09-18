from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Populates the database with fake data for development and testing.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        fake = Faker()

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.filter(is_superuser=False).delete()

        # Create Users
        self.stdout.write('Creating users...')
        users = []
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{last_name.lower()}"
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            password = 'password123'
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
