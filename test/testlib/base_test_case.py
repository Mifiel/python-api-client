from unittest import TestCase

class BaseTestCase(TestCase):
  """
  from http://blog.aaronboman.com/programming
    /testing/2016/02/11/how-to-write-tests-in-python-project-structure/
  All test cases should inherit from this class as any common
  functionality that is added here will then be available to all
  subclasses. This facilitates the ability to update in one spot
  and allow all tests to get the update for easy maintenance.
  """
