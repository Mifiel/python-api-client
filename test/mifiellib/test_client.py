from mifiel import Client
from mifiel.user_agent import build_user_agent
from mifiellib import BaseMifielCase

class TestClient(BaseMifielCase):
  def setUp(self):
    self.client = Client('app_id', 'secret')

  def test_url(self):
    self.assertRegex(self.client.url(), 'app.mifiel.com')

  def test_sandbox(self):
    self.client.use_sandbox()
    self.assertRegex(self.client.url(), 'app-sandbox.mifiel.com')

  def test_base_url(self):
    self.client.set_base_url('http://example.com')
    self.assertRegex(self.client.url(), 'example.com')

  def test_timeout(self):
    self.client.set_timeout(timeout=4)
    self.assertEqual(self.client.timeout, 4)

  def test_user_agent(self):
    ua = build_user_agent()
    parts = ua.split(' ')
    self.assertTrue(parts[0].startswith('PYTHON/'))
    self.assertTrue(parts[1].startswith('mifiel/'))
    self.assertTrue(parts[2].startswith('requests/'))
    self.assertTrue(parts[3].startswith('(') and parts[3].endswith(')'))
