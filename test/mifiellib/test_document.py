from mifiel import Document
from mifiellib import BaseMifielCase

import json
import responses

class TestDocument(BaseMifielCase):
  def setUp(self):
    super(TestDocument, self).setUp()
    self.doc = Document(self.client)

  def mock_doc_response(self, method, url, doc_id):
    responses.add(
      method=method,
      url=url,
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
    url = self.client.url().format(path='documents/' + doc_id)
    self.mock_doc_response(responses.GET, url, doc_id)

    doc = Document.find(self.client, doc_id)

    req = self.get_last_request()
    self.assertEqual(req.body, None)
    self.assertEqual(req.method, 'GET')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    self.assertEqual(doc.callback_url, 'some')
    assert req.headers['Authorization'] is not None

  @responses.activate
  def test_update(self):
    doc_id = 'some-doc-id'
    url = self.client.url().format(path='documents/' + doc_id)
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

  def test_update_without_id(self):
    doc = Document(self.client)
    doc.callback_url = 'some-callback'
    self.assertFalse(doc.save())

  @responses.activate
  def test_create(self):
    doc_id = 'some-doc-id'
    url = self.client.url().format(path='documents')
    self.mock_doc_response(responses.POST, url, doc_id)

    signatories = [{'email': 'some@email.com'}]
    doc = Document.create(self.client, signatories, dhash='some-sha256-hash')

    req = self.get_last_request()
    self.assertEqual(req.method, 'POST')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    self.assertEqual(doc.callback_url, 'some')
    assert req.headers['Authorization'] is not None

  def test_create_without_file_or_hash(self):
    with self.assertRaises(ValueError):
      Document.create(self.client, [])

  def test_create_with_file_and_hash(self):
    with self.assertRaises(ValueError):
      Document.create(self.client, [], dhash='dhash', file='file')
