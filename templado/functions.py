import os
import errno
from django.conf import settings

def get_absolute_directory(relativeDirectory):
    return os.path.join(settings.MEDIA_ROOT, relativeDirectory)

def get_and_create_absolute_directory(relativeDirectory):
    directory = get_absolute_directory(relativeDirectory)
    try:
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return directory


def get_uploaded_static_files():
    return os.listdir(get_and_create_absolute_directory(settings.TEMPLADO_REPORT_STATIC_DIR))


def save_static_file(f):
    directory = get_and_create_absolute_directory(settings.TEMPLADO_REPORT_STATIC_DIR)
    filename = f.name.split('/')[-1]
    with open(os.path.join(directory, filename), 'w') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
