import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from api.models import Ingredients, Tags


def ingredients():
    """Добавление ингредиента в БД, если его в ней нет."""
    with open(os.path.join(settings.BASE_DIR, 'data', 'ingredients.json'),
              'r', encoding='utf-8') as file:
        data = json.load(file)
        ls_ing = []
        for i in range(len(data)):
            new = Ingredients(
                name=data[i].get("name"),
                measurement_unit=data[i].get("measurement_unit"))
            ls_ing.append(new)
        Ingredients.objects.bulk_create(ls_ing, ignore_conflicts=True)


def tags():
    """Добавление тэга в БД, если его в ней нет."""
    with open(os.path.join(settings.BASE_DIR, 'data', 'tags.json'),
              'r', encoding='utf-8') as file:
        data = json.load(file)
        ls_tags = []
        for i in range(len(data)):
            new = Tags(
                name=data[i].get("name"),
                color=data[i].get("color"),
                slug=data[i].get("slug"),
            )
            ls_tags.append(new)
        Tags.objects.bulk_create(ls_tags, ignore_conflicts=True)


class Command(BaseCommand):

    def handle(self, *args, **options):
        ingredients()
        tags()
