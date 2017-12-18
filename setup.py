#!/usr/bin/env python3
from setuptools import setup

setup(name='juice',
      version='0.1',
      description='A Python frontend to the Squeezebox CLI',
      author='OldIronHorse',
      author_email='',
      license='GPL 3.0',
      packages=['juice'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
