from os.path import dirname, join
import sys

import django
import django.conf


def pytest_configure():
    example_path = join(dirname(dirname(__file__)), 'example')
    if example_path not in sys.path:
        sys.path.insert(0, example_path)
    settings = {
        'ALLOWED_HOSTS': ['testserver'],
        'DEBUG': True,
        'MIDDLEWARE_CLASSES': [
            'django_httpolice.HTTPoliceMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        'ROOT_URLCONF': 'example_project.urls',
        'LANGUAGE_CODE': 'en-us',
        'USE_I18N': False,
        'HTTPOLICE_ENABLE': True,
        'HTTPOLICE_SILENCE': [1070, 1110],
    }
    if django.VERSION >= (1, 10):   # pragma: no cover
        settings['MIDDLEWARE'] = settings.pop('MIDDLEWARE_CLASSES')
    django.conf.settings.configure(**settings)
