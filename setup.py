# -*- coding: utf-8; -*-

import io
import os

from setuptools import setup


metadata = {}
with io.open(os.path.join('django_httpolice', '__metadata__.py'), 'rb') as f:
    exec(f.read(), metadata)            # pylint: disable=exec-used

with io.open('README.rst') as f:
    long_description = f.read()


setup(
    name='Django-HTTPolice',
    version=metadata['version'],
    description='Django integration for HTTPolice',
    long_description=long_description,
    url='https://github.com/vfaronov/django-httpolice',
    author='Vasiliy Faronov',
    author_email='vfaronov@gmail.com',
    license='MIT',
    python_requires='>= 3.4',
    install_requires=[
        'Django >= 1.11.0',
        'HTTPolice >= 0.4.0',
    ],
    packages=['django_httpolice'],
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Quality Assurance',
    ],
    keywords='HTTP message request response standards RFC validator Django',
)
