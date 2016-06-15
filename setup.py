from setuptools import setup

try:
  import pypandoc
  long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
  long_description = open('README.md').read()

setup(name='mifiel',
      version='0.0.1',
      description='Python API Client library for Mifiel.com',
      long_description=long_description,
      url='http://github.com/mifiel/python-api-client',
      author='Genaro Madrid',
      author_email='genmadrid@gmail.com',
      license='MIT',
      test_suite='nose2.collector.collector',
      packages=['mifiel'],
      install_requires=[
        'requests'
      ],
      include_package_data=True,
      zip_safe=False)
