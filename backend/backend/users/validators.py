from django.core.exceptions import ValidationError

import re


FORBIDDEN_USERNAME = 'me'
FORBIDDEN_LETTERS = r'^[\w.@+-]+\Z'

set_of_forbidden_letters = set()


def validate_forbidden_username(value):
    if value == FORBIDDEN_USERNAME:
        raise ValidationError(
            f'Имя пользователя не может быть {value}')
    set_of_forbidden_letters.clear()
    for letter in list(value):
        if re.match(FORBIDDEN_LETTERS, letter) is None:
            set_of_forbidden_letters.add(letter)
    if set_of_forbidden_letters:
        raise ValidationError(
            f'Имя пользователя не может содержать {set_of_forbidden_letters}')
    return value
