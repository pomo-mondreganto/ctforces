import os
import re
import uuid
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import UserManager
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum, Q, Value as V, FileField, F, Count, Avg
from django.db.models.functions import Coalesce, Greatest, Ceil, Sqrt
from django.utils.deconstruct import deconstructible
from rest_framework import exceptions

from api.celery_tasks import process_stdimage


@deconstructible
class CustomASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w_-]{3,15}$'
    message = (
        'Username needs to contain from 3 to 15 English letters, '
        'numbers, and -/_ characters'
    )
    flags = re.ASCII


@deconstructible
class TagNameValidator(validators.RegexValidator):
    regex = '^[a-z0-9]+(-[a-z0-9]+)*[a-z0-9]+$'
    message = 'Name must consist of words (lowercase letters and digits), divided my single dash'


class UserUpsolvingAnnotatedManager(UserManager):
    def get_queryset(self):
        return super(UserUpsolvingAnnotatedManager, self).get_queryset().annotate(
            cost_sum=Coalesce(
                Sum(
                    'solved_tasks__cost',
                    filter=Q(solved_tasks__show_on_main_page=True),
                ),
                V(0),
            )
        )


class TeamRatingAnnotatedManager(models.Manager):
    def get_queryset(self):
        qs = super(TeamRatingAnnotatedManager, self).get_queryset()
        return qs.prefetch_related(
            'participants',
        ).annotate(
            rating=Sqrt(
                Avg(F('participants__rating') ** 2, distinct=True),
            ),
        )


class CTRCurrentCostManager(models.Manager):
    def __init__(self, dynamic):
        super(CTRCurrentCostManager, self).__init__()
        self.dynamic = dynamic

    def get_queryset(self):
        qs = super(CTRCurrentCostManager, self).get_queryset()
        if self.dynamic:
            qs = qs.annotate(
                solved_count=Coalesce(
                    Count(
                        'solved_by',
                        distinct=True,
                    ),
                    V(0),
                ),
                current_cost=Greatest(
                    Ceil(
                        (F('min_cost') - F('max_cost')) /
                        (F('decay_value') * F('decay_value')) *
                        (F('solved_count') * F('solved_count')) +
                        F('max_cost')
                    ),
                    F('min_cost'),
                ),
            )
        else:
            qs = qs.annotate(
                solved_count=Coalesce(
                    Count(
                        'solved_by',
                        distinct=True,
                    ),
                    V(0),
                ),
                current_cost=F('cost'),
            )

        return qs


@deconstructible
class CustomUploadTo:
    path_pattern = "{path}/{upload_type}"
    file_pattern = "{name}{ext}"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, instance, filename):
        path, ext = os.path.splitext(filename)
        path, name = os.path.split(path)
        defaults = {
            'ext': ext,
            'name': name,
            'path': path,
            'upload_type': 'other',
        }
        defaults.update(self.kwargs)
        if self.kwargs.get('random_filename'):
            defaults['name'] = uuid.uuid4().hex
        if self.kwargs.get('append_random'):
            random_str = uuid.uuid4().hex
            defaults['name'] = f'{defaults["name"]}_{random_str}'
        result = os.path.join(self.path_pattern.format(**defaults), self.file_pattern.format(**defaults)).lstrip('/')

        return result


@deconstructible
class CustomImageSizeValidator:

    def __init__(self, min_limit, max_limit, ratio):
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.ratio_limit = ratio

    @staticmethod
    def clean(value):
        value.seek(0)
        stream = BytesIO(value.read())
        img = Image.open(stream)
        return img.size

    def __call__(self, value):
        cleaned = self.clean(value)
        if self.compare_min(cleaned, self.min_limit):
            params = {
                'width': self.min_limit[0],
                'height': self.min_limit[1],
            }
            raise ValidationError('Your image is too small. '
                                  'The minimal resolution is {width}x{height}'.format(**params),
                                  code='min_resolution')
        if self.compare_max(cleaned, self.max_limit):
            params = {
                'width': self.max_limit[0],
                'height': self.max_limit[1],
            }
            raise ValidationError('Your image is too big. '
                                  'The maximal resolution is {width}x{height}'.format(**params),
                                  code='max_resolution')

        if self.compare_ratio(cleaned, self.ratio_limit):
            params = {
                'ratio': self.ratio_limit,
            }
            raise ValidationError('Your image is too unbalanced. '
                                  'The maximal ratio is {ratio}'.format(**params),
                                  code='ratio')

    @staticmethod
    def compare_min(img_size, min_size):
        return img_size[0] < min_size[0] or img_size[1] < min_size[1]

    @staticmethod
    def compare_max(img_size, max_size):
        return img_size[0] > max_size[0] or img_size[1] > max_size[1]

    @staticmethod
    def compare_ratio(img_size, ratio):
        return img_size[0] * ratio <= img_size[1] or img_size[1] * ratio <= img_size[0]


def stdimage_processor(file_name, variations, storage):
    process_stdimage.delay(file_name, variations, storage)
    return False


class CustomFileField(FileField):

    def __init__(self, *args, **kwargs):
        self.max_file_size = kwargs.pop('max_file_size', settings.MAX_FILE_SIZE)
        super(CustomFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(CustomFileField, self).clean(*args, **kwargs)
        file = data.file
        if file.size > self.max_file_size:
            raise exceptions.ValidationError(f'File size must be under {self.max_file_size // 1024 // 1024}MB.')
        return data
