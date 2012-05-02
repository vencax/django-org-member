#!/usr/bin/env python
from setuptools import setup, find_packages
import os

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README')

description = 'Manages organization members and their attendance on events.'

if os.path.exists(README_PATH):
    long_description = open(README_PATH).read()
else:
    long_description = description

setup(name='django-org-member',
    version='',
    description=description,
    license='BSD',
    url='https://github.com/vencax/django-org-member',
    author='vencax',
    author_email='vencax@centrum.cz',
    packages=find_packages(),
    install_requires=[
        'django>=1.4',
        'south',
        'feincms-groupagenda',
    ],
    keywords="django organisation management crm",
    include_package_data=True,
)
