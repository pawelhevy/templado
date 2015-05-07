import os
import errno
from django.conf import settings


def get_static_directory():
    directory = settings.REPORT_STATIC_DIR
    try:
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return directory


def get_uploaded_static_files():
    return os.listdir(get_static_directory())


def save_static_file(f):
    directory = get_static_directory()
    filename = f.name.split('/')[-1]
    with open(os.path.join(directory, filename), 'w') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
