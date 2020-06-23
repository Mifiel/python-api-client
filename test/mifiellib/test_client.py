from mifiel import Client
from mifiellib import BaseMifielCase

class TestClient(BaseMifielCase):
  def setUp(self):
    self.client = Client('app_id', 'secret')

  def test_url(self):
    self.assertRegex(self.client.url(), 'www.mifiel')

  def test_sandbox(self):
    self.client.use_sandbox()
    self.assertRegex(self.client.url(), 'sandbox.mifiel')

  def test_base_url(self):
    self.client.set_base_url('http://example.com')
    self.assertRegex(self.client.url(), 'example.com')

  def test_timeout(self):
    self.client.set_timeout(timeout=4)
    self.assertEqual(self.client.timeout, 4)
