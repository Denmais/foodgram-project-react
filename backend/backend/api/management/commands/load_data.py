import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Ingredients, Tags


def ingredients():
    with open(os.path.join(settings.BASE_DIR, 'data', 'ingredients.json'),
              'r', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(len(data)):
            Ingredients.objects.get_or_create(
                name=data[i].get("name"),
                measurement_unit=data[i].get("measurement_unit")
            )


def tags():
    with open(os.path.join(settings.BASE_DIR, 'data', 'tags.json'),
              'r', encoding='utf-8') as file:
        data = json.load(file)
        for i in range(len(data)):
            Tags.objects.get_or_create(
                name=data[i].get("name"),
                color=data[i].get("color"),
                slug=data[i].get("slug"),
            )


class Command(BaseCommand):

    def handle(self, *args, **options):
        ingredients()
        tags()
