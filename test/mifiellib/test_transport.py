import io
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
import requests
import responses

from mifiel import Base, Client, Document, Template, Webhook


@pytest.fixture
def client():
  client = Client('test-app-id', 'test-secret')
  client.set_base_url('http://localhost:3000')
  return client


@responses.activate
@pytest.mark.parametrize('resource', [Document, Template])
def test_save_sends_changed_attributes(client, resource):
  obj = resource(client)
  obj.id = 'resource-id'
  obj.callback_url = 'https://example.com/callback'
  responses.put(obj.url(obj.id), json={'id': obj.id})

  obj.save()

  assert parse_qs(responses.calls[0].request.body)['callback_url'] == [
    'https://example.com/callback',
  ]


@responses.activate
@pytest.mark.parametrize('method', ['post', 'put'])
@pytest.mark.parametrize('as_pairs', [False, True])
def test_form_values_preserve_false_zero_and_empty_strings(client, method, as_pairs):
  base = Base(client, 'documents')
  responses.add(method.upper(), base.url(), json={})
  data = {'send_invites': False, 'remind_every': 0, 'name': '', 'active': True}
  if as_pairs:
    data = list(data.items())

  base.execute_request(method, data=data)

  assert parse_qs(responses.calls[0].request.body, keep_blank_values=True) == {
    'send_invites': ['false'], 'remind_every': ['0'], 'name': [''], 'active': ['true'],
  }


@responses.activate
def test_get_parameters_are_signed_in_url(client):
  base = Base(client, 'documents')
  responses.get(base.url(), json=[])
  base.execute_request('get', params={'page': 2, 'name': 'a b'})
  request = responses.calls[0].request
  assert parse_qs(urlparse(request.url).query) == {'page': ['2'], 'name': ['a b']}
  assert request.body is None
  assert request.headers['Authorization'].startswith('APIAuth test-app-id:')


@responses.activate
@pytest.mark.parametrize('method', ['get', 'post', 'put', 'delete'])
def test_http_errors_raise_before_returning_json(client, method):
  base = Base(client, 'documents')
  responses.add(method.upper(), base.url(), json={'error': 'denied'}, status=403)
  with pytest.raises(requests.HTTPError) as error:
    base.execute_request(method)
  assert error.value.response.status_code == 403


@responses.activate
@pytest.mark.parametrize('resource', [Document, Template, Webhook])
def test_collection_errors_do_not_become_resource_lists(client, resource):
  responses.get(resource(client).url(), json={'error': 'unauthorized'}, status=401)
  with pytest.raises(requests.HTTPError):
    resource.all(client)


def test_upload_is_closed_when_connection_fails(client):
  upload = io.BytesIO(b'pdf data')
  with (patch('mifiel.base.requests.post', side_effect=requests.ConnectionError),
        pytest.raises(requests.ConnectionError)):
    Base(client, 'documents').execute_request('post', files={'file': ('file.pdf', upload)})
  assert upload.closed


@responses.activate
def test_create_upload_does_not_send_local_path_as_a_form_field(client, tmp_path):
  path = tmp_path / 'local-private-name.pdf'
  path.write_bytes(b'%PDF-1.4\n')
  responses.post(Document(client).url(), json={'id': 'document-id'})
  Document.create(client, [{'email': 'signer@example.com'}], file=path, send_invites=False)
  body = responses.calls[0].request.body
  assert body.count(b'name="file"') == 1
  assert str(path).encode() not in body
  assert b'\r\nfalse\r\n' in body


def test_explicit_timeout_reaches_every_request_method(client):
  client.set_timeout(12)
  for method in ['get', 'post', 'put', 'delete']:
    with patch('mifiel.base.requests.' + method) as send:
      Base(client, 'documents').execute_request(method)
    assert send.call_args.kwargs['timeout'] == 12


def test_unknown_method_fails_before_network(client):
  with pytest.raises(ValueError, match='Unsupported'):
    Base(client, 'documents').execute_request('invalid')
