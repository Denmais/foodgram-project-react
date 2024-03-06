import webcolors
from django.core.exceptions import ValidationError


def validate_color(value):
    try:
        print(value)
        webcolors.hex_to_name(value)
    except ValueError:
        raise ValidationError('Для этого цвета нет имени')
