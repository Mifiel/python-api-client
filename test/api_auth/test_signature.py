from mifiel.api_auth import Signature
from testlib import BaseTestCase

import datetime

class TestApiAuthSignature(BaseTestCase):
  def setUp(self):
    self.sig = Signature('secret_key')

  def test_build(self):
    d = datetime.date.fromordinal(735999)
    httpdate = d.strftime('%a, %d %b %Y %H:%M:%S GMT')
    self.sig.build(
      method='GET',
      url='http://some-url.com',
      body='some-body',
      content_type='text/json',
      httpdate=httpdate
    )
    self.assertEqual(self.sig.signature, 'T9lDIpknHXt1jDcoiU0YnHi4flA=')

  def test_build2(self):
    d = datetime.date.fromordinal(735999)
    httpdate = d.strftime('%a, %d %b %Y %H:%M:%S GMT')
    self.sig.build(
      method='GET',
      url='http://www.some-url.com',
      body='',
      content_type='text/json',
      httpdate=httpdate
    )
    self.assertEqual(self.sig.signature, 'Z+e8CG9ZGQ0YFxrKEYltxVu4tRU=')
