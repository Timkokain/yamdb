from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(data):
    if data > timezone.now().year:
        raise ValidationError('Произведение ещё не вышло!')
