from mifiel import Template
from mifiellib import BaseMifielCase

import json
import responses
import os.path

class TestTemplate(BaseMifielCase):
  def setUp(self):
    super(TestTemplate, self).setUp()
    self.tmpl = Template(self.client)

  def mock_tmpl_response(self, method, url, tmpl_id):
    responses.add(
      method=method,
      url=url,
      body=json.dumps({
        'id': tmpl_id,
        'name': 'some name'
      }),
      status=200,
      content_type='application/json',
    )

  @responses.activate
  def test_get(self):
    tmpl_id = 'some-tmpl-id'
    url = self.client.url().format(path='templates/' + tmpl_id)
    self.mock_tmpl_response(responses.GET, url, tmpl_id)

    tmpl = Template.find(self.client, tmpl_id)

    req = self.get_last_request()
    self.assertEqual(req.body, None)
    self.assertEqual(req.method, 'GET')
    self.assertEqual(req.url, url)
    self.assertEqual(tmpl.id, tmpl_id)
    assert req.headers['Authorization'] is not None

  @responses.activate
  def test_all(self):
    url = self.client.url().format(path='templates')
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

    docs = Template.all(self.client)
    self.assertEqual(len(docs), 1)

  @responses.activate
  def test_delete(self):
    url = self.client.url().format(path='templates')
    url = '{}/{}'.format(url, 'some-doc-id')
    responses.add(
      method=responses.DELETE,
      url=url,
      body=json.dumps({
        'status': 'success',
        'message': 'Destroyed document#some-doc-id',
        'data': { 'id': 'some-doc-id'}
      }),
      status=200,
      content_type='application/json',
    )
    response = Template.delete(self.client, 'some-doc-id')
    self.assertEqual(response['status'], 'success')

  @responses.activate
  def test_update(self):
    tmpl_id = 'some-tmpl-id'
    url = self.client.url().format(path='templates/' + tmpl_id)
    self.mock_tmpl_response(responses.PUT, url, tmpl_id)

    tmpl = Template(self.client)
    tmpl.id = tmpl_id
    tmpl.random_param = 'random-param'
    tmpl.other_param = 'other-param'
    tmpl.save()

    req = self.get_last_request()
    self.assertEqual(req.method, 'PUT')
    self.assertEqual(req.url, url)
    self.assertEqual(tmpl.id, tmpl_id)
    assert req.headers['Authorization'] is not None

  def test_update_without_id(self):
    tmpl = Template(self.client)
    tmpl.callback_url = 'some-callback'
    self.assertFalse(tmpl.save())

  @responses.activate
  def test_create(self):
    tmpl_id = 'some-tmpl-id'
    url = self.client.url().format(path='templates')
    self.mock_tmpl_response(responses.POST, url, tmpl_id)

    content = '<div>' \
                 'Name <field name="name" type="text">NAME</field>' \
                 'Date <field name="date" type="text">DATE</field>' \
               '</div>'
    tmpl = Template.create(
      client=self.client,
      name='mywhheehss1o',
      description='Confidential disclosure agreement',
      header='<div>some header html</div>',
      content=content,
      footer='<div>some footer html</div>'
    )

    req = self.get_last_request()
    self.assertEqual(req.method, 'POST')
    self.assertEqual(req.url, url)
    self.assertEqual(tmpl.id, tmpl_id)
    assert req.headers['Authorization'] is not None
