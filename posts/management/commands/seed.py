from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from posts import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Not implemented yet...")