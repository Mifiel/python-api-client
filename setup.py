from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='mifiel',
      version='0.0.1',
      description='mifiel.com API Client',
      long_description=readme(),
      url='http://github.com/mifiel/python-api-client',
      download_url='https://github.com/Mifiel/python-api-client/tarball/0.0.1',
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
