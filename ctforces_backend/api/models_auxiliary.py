import os
import uuid
from django.utils.deconstruct import deconstructible


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
