from mifiel import Document
from mifiellib import BaseMifielCase

import responses
import os.path

try:
  import simplejson as json
except ImportError:
  import json

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
  def test_all(self):
    url = self.client.url().format(path='documents')
    responses.add(
      method=responses.GET,
      url=url,
      body=json.dumps([{
        'id': 'some-doc-id',
        'callback_url': 'some'
      }]),
      status=200,
      content_type='application/json',
    )

    docs = Document.all(self.client)
    self.assertEqual(len(docs), 1)

  @responses.activate
  def test_delete_empty_response(self):
    url = self.client.url().format(path='documents')
    url = '{}/{}'.format(url, 'some-doc-id')
    responses.add(
      method=responses.DELETE,
      url=url,
      body='',
      status=205,
      content_type='application/json',
    )
    response = Document.delete(self.client, 'some-doc-id')
    self.assertEqual(response['status'], 'success')

  @responses.activate
  def test_delete_json_response(self):
    url = self.client.url().format(path='documents')
    url = '{}/{}'.format(url, 'some-doc-id')
    responses.add(
      method=responses.DELETE,
      url=url,
      body=json.dumps({
        'status': 'success',
        'message': 'Destroyed document#some-doc-id',
        'data': {'id': 'some-doc-id'}
      }),
      status=200,
      content_type='application/json',
    )
    response = Document.delete(self.client, 'some-doc-id')
    self.assertEqual(response['status'], 'success')

  @responses.activate
  def test_create(self):
    doc_id = 'some-doc-id'
    url = self.client.url().format(path='documents')
    self.mock_doc_response(responses.POST, url, doc_id)

    signatories = [{'email': 'some@email.com'}]
    doc = Document.create(self.client, signatories, dhash='some-sha256-hash', name='some.pdf')

    req = self.get_last_request()
    self.assertEqual(req.method, 'POST')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    self.assertEqual(doc.callback_url, 'some')
    assert req.headers['Authorization'] is not None

  @responses.activate
  def test_create_with_file(self):
    doc_id = 'some-doc-id'
    url = self.client.url().format(path='documents')
    self.mock_doc_response(responses.POST, url, doc_id)

    signatories = [
      {'email': 'some@email.com', 'tax_id': 'ASDD543412ERP'},
      {'email': 'some@email1.com', 'tax_id': 'ASDD543413ERP'}
    ]
    doc = Document.create(
      client=self.client,
      signatories=signatories,
      file='test/fixtures/example.pdf',
      callback_url='https://www.example.com'
    )

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

  @responses.activate
  def test_save_file(self):
    doc_id = '8600153a-4845-4d11-aac6-1d3d6048e022'
    url = self.client.url().format(path='documents')
    url = '{}/{}/file'.format(url, doc_id)
    responses.add(
      method=responses.GET,
      url=url,
      body='some-pdf-contents',
      status=200,
      content_type='application/pdf',
    )
    doc = Document(self.client)
    doc.id = doc_id
    path = 'tmp/the-file.pdf'
    doc.save_file(path)
    req = self.get_last_request()
    self.assertEqual(req.method, 'GET')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    assert req.headers['Authorization'] is not None
    self.assertTrue(os.path.isfile(path))

  @responses.activate
  def test_save_file_signed(self):
    doc_id = '8600153a-4845-4d11-aac6-1d3d6048e022'
    url = self.client.url().format(path='documents')
    url = '{}/{}/file_signed'.format(url, doc_id)
    responses.add(
      method=responses.GET,
      url=url,
      body='some-pdf-contents',
      status=200,
      content_type='application/pdf',
    )
    doc = Document(self.client)
    doc.id = doc_id
    path = 'tmp/the-file-signed.pdf'
    doc.save_file_signed(path)
    req = self.get_last_request()
    self.assertEqual(req.method, 'GET')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    assert req.headers['Authorization'] is not None
    self.assertTrue(os.path.isfile(path))

  @responses.activate
  def test_create_from_template(self):
    tmpl_id = 'ce734d7d-e259-4b7a-b1d8-a5ea8fdcbea1'
    doc_id = '8600153a-4845-4d11-aac6-1d3d6048e022'
    url = self.client.url().format(path='templates')
    url = '{}/{}/generate_document'.format(url, tmpl_id)
    self.mock_doc_response(responses.POST, url, doc_id)

    args = {
      'template_id': tmpl_id,
      'name': 'My NDA',
      'fields': {
        'name': 'My Client Name',
        'date': 'Sep 27 2017'
      },
      'signatories': [{
        'name': 'Some name',
        'email': 'some@email.com',
        'tax_id': 'AAA010101AAA'
      }],
      'callback_url': 'https://www.example.com/webhook/url',
      'external_id': 'unique-id'
    }
    doc = Document.create_from_template(self.client, args)
    req = self.get_last_request()
    self.assertEqual(req.method, 'POST')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    assert req.headers['Authorization'] is not None

  @responses.activate
  def test_create_many_from_template(self):
    tmpl_id = 'ce734d7d-e259-4b7a-b1d8-a5ea8fdcbea1'
    doc_id = '8600153a-4845-4d11-aac6-1d3d6048e022'
    url = self.client.url().format(path='templates')
    url = '{}/{}/generate_documents'.format(url, tmpl_id)
    responses.add(
      method=responses.POST,
      url=url,
      body=json.dumps({ 'status': 'success' }),
      status=200,
      content_type='application/json',
    )

    args = {
      'template_id': tmpl_id,
      'identifier': 'name',
      'callback_url': 'https://www.my-site.com/documents-ready',
      'documents': [{
        'fields': {
          'name': 'My Client Name',
          'date': 'Sep 27 2017'
        },
        'signatories': [{
          'name': 'Some Name',
          'email': 'some@email.com',
          'tax_id': 'AAA010101AAA'
        }],
        'callback_url': 'https://www.my-site.com/sign-webhook',
        'external_id': 'uniques-id2'
      }]
    }
    response = Document.create_many_from_template(self.client, args)
    req = self.get_last_request()
    self.assertEqual(req.method, 'POST')
    self.assertEqual(req.url, url)
    self.assertEqual(response['status'], 'success')
    assert req.headers['Authorization'] is not None

  @responses.activate
  def test_save_xml(self):
    doc_id = '8600153a-4845-4d11-aac6-1d3d6048e022'
    url = self.client.url().format(path='documents')
    url = '{}/{}/xml'.format(url, doc_id)
    responses.add(
      method=responses.GET,
      url=url,
      body='<some><xml><contents /></xml></some>',
      status=200,
      content_type='application/xml',
    )
    doc = Document(self.client)
    doc.id = doc_id
    path = 'tmp/the-file.xml'
    doc.save_xml(path)
    req = self.get_last_request()
    self.assertEqual(req.method, 'GET')
    self.assertEqual(req.url, url)
    self.assertEqual(doc.id, doc_id)
    assert req.headers['Authorization'] is not None
    self.assertTrue(os.path.isfile(path))
