import datetime as dt

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > dt.datetime.now().year:
        raise ValidationError('Нельзя добавлять произведения, которых еще нет')
