from setuptools import setup

def readme():
  with open('README.md') as f:
    return f.read()

setup(name='mifiel',
      version='0.0.0',
      description='The funniest joke in the world',
      long_description=readme(),
      url='http://github.com/mifiel/python-api-client',
      author='Genaro Madrid',
      author_email='genmadrid@gmail.com',
      license='MIT',
      packages=['mifiel'],
      install_requires=[
        'requests'
      ],
      include_package_data=True,
      zip_safe=False)
