import os
import uuid
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import FileField
from django.utils.deconstruct import deconstructible
from rest_framework import exceptions

from .tasks import process_stdimage


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
            defaults['name'] = '{}_{}'.format(defaults['name'], uuid.uuid4().hex)
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
            raise exceptions.ValidationError('File size must be under {}MB.'.format(self.max_file_size // 1024 // 1024))
        return data
