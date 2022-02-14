from datetime import date

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def only_letters(value):
    # for ch in value:
    #     if not ch.isalpha():
    #         raise ValidationError('Value must contain only letters!')
    if not all(ch.isalpha() for ch in value):  # invalid
        raise ValidationError('Value must contain only letters!')
    # valid -> not need to return


def file_max_size(value):
    max_size = 5
    filesize = value.file.size
    if filesize > max_size * 1024 * 1024:
        raise ValidationError(f'File max size is {max_size}MB.')


def correct_date(value):
    start_date = date(1920, 1, 1)
    if value < start_date or value > date.today():
        raise ValidationError(f'The date must be later than 1920-1-1 and earlier today!')


@deconstructible
class MinDateValidator:  # class validator with callback
    def __init__(self, min_date):
        self.min_date = min_date

    def __call__(self, value):
        if self.min_date > value:
            raise ValidationError(f'The date must be later than {self.min_date}!')