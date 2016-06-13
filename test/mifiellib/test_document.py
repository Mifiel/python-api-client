from mifiel import Document
from mifiellib import BaseMifielCase

import json
import responses

class TestDocument(BaseMifielCase):
  def setUp(self):
    super().setUp()
    self.doc = Document(self.client)

  def mock_doc_response(self, merhod, url, doc_id):
    responses.add(merhod, url,
      body=json.dumps({
        'id': doc_id,
        'callback_url': 'some'
      }),
      status=200,
      content_type='application/json',
    )

  @responses.activate
  def test_get(self):
    doc_id = 'some-doc-id'
    url = self.client.url().format(path='documents/'+doc_id)
    self.mock_doc_response(responses.GET, url, doc_id)

    doc = Document.get(self.client, doc_id)

    req = self.get_last_request()
    self.assertEqual(req.body, None)
    self.assertEqual(req.method, 'GET')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    self.assertEqual(doc.callback_url, 'some')
    assert req.headers['Authorization'] is not None

  @responses.activate
  def test_save(self):
    doc_id = 'some-doc-id'
    url = self.client.url().format(path='documents/'+doc_id)
    self.mock_doc_response(responses.PUT, url, doc_id)

    doc = Document(self.client)
    doc.id = doc_id
    doc.callback_url = 'some-callback'
    doc.random_param = 'random-param'
    doc.other_param = 'other-param'
    doc.save()

    req = self.get_last_request()
    self.assertEqual(req.method, 'PUT')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    self.assertEqual(doc.callback_url, 'some')
    assert req.headers['Authorization'] is not None

