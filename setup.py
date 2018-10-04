from setuptools import setup

try:
  long_description = open('README.txt').read()
except(IOError, ImportError):
  long_description = open('README.md').read()

setup(
  name='mifiel',
  version='0.0.5',
  description='Python API Client library for Mifiel.com',
  long_description=long_description,
  url='http://github.com/mifiel/python-api-client',
  download_url='https://github.com/Mifiel/python-api-client/tarball/v0.0.5',
  author='Genaro Madrid',
  author_email='genmadrid@gmail.com',
  license='MIT',
  test_suite='nose2.collector.collector',
  packages=['mifiel', 'mifiel.api_auth'],
  install_requires=[
    'requests'
  ],
  include_package_data=True,
  zip_safe=False
)
