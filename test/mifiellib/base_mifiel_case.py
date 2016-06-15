from testlib import BaseTestCase

from mifiel import Client

import responses

class BaseMifielCase(BaseTestCase):
  def setUp(self):
    app_id = '836dd40b613ffb1bb06585bdc57638ff0ff2dbc0'
    secret_key = ('rkV4tj1sHxUM26OJpr2MK5U2re4luERo/SmXB1s6o/'
                  'l9G/Ei4rFKrrArhEKMIufQgndZXaIywX05tPN2OvPt7w==')
    self.client = Client(app_id, secret_key)
    # Ensure no requests to mifiel servers
    self.client.set_base_url('http://localhost:3000')

  def get_last_request(self):
    return responses.calls[0].request
