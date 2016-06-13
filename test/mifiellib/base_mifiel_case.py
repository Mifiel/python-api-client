from testlib import BaseTestCase

from mifiel import Client

import responses

class BaseMifielCase(BaseTestCase):
  """
  from http://blog.aaronboman.com/programming/testing/2016/02/11/how-to-write-tests-in-python-project-structure/
  All test cases should inherit from this class as any common
  functionality that is added here will then be available to all
  subclasses. This facilitates the ability to update in one spot
  and allow all tests to get the update for easy maintenance.
  """

  def setUp(self):
    app_id = '836dd40b613ffb1bb06585bdc57638ff0ff2dbc0'
    secret_key = 'rkV4tj1sHxUM26OJpr2MK5U2re4luERo/SmXB1s6o/l9G/Ei4rFKrrArhEKMIufQgndZXaIywX05tPN2OvPt7w=='
    self.client = Client(app_id, secret_key)
    # Ensure no requests to mifiel servers
    self.client.set_base_url('http://localhost:3000')

  def get_last_request(self):
    return responses.calls[0].request
