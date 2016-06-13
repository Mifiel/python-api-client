from mifiel.api_auth import RequestsApiAuth
from testlib import BaseTestCase

import base64, hashlib
import responses
import requests

class TestApiAuth(BaseTestCase):
  def setUp(self):
    self.access_id = 'access_id'
    self.secret_key = 'secret_key'
    self.api_auth = RequestsApiAuth(self.access_id, self.secret_key)

  def make_request(self, path, query=None):
    url = 'http://example.com/api/v1/{path}'.format(path=path)
    if query: url += '?{query}'.format(query=query)
    responses.add(**{
      'method'         : responses.GET,
      'url'            : url,
      'body'           : '{"ok": "all ok"}',
      'status'         : 200,
      'content_type'   : 'application/json',
      'match_querystring': True
    })
    requests.get(url, auth=self.api_auth, data=query)

  def get_last_headers(self):
    return responses.calls[0].request.headers

  @responses.activate
  def test_request(self):
    self.make_request('blah')
    m = hashlib.md5()
    m.update(''.encode('ascii'))
    empty_md5 = base64.b64encode(m.digest()).decode()
    headers = self.get_last_headers()
    self.assertEqual(headers['content-md5'], empty_md5)
    assert headers['Authorization'] is not None

  @responses.activate
  def test_request_with_query(self):
    self.make_request('blah', 'some=query')
    headers = self.get_last_headers()
    assert headers['Authorization'] is not None
