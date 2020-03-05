import os

from django.conf import settings
from djangorestframework_camel_case.util import camel_to_underscore

from core.data import ABILITY_DICT


def get_ability_name(key):
    return ABILITY_DICT[key]


def portrait_upload_to(instance, file_name):
    class_name = camel_to_underscore(instance.__class__.__name__).strip('_')
    _, extension = os.path.splitext(file_name)
    new_file_name = '{}{}'.format(instance.id, extension)
    path = os.path.join(class_name, 'portrait', str(instance.id), new_file_name)
    # Remove previous file
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(media_path):
        os.remove(media_path)
    return path
