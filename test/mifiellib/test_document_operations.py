import io
import json
import zipfile
from unittest.mock import patch

import pytest
import requests
import responses

from mifiel import Client, Document


@pytest.fixture
def document():
  client = Client('test-app-id', 'test-secret')
  client.set_base_url('http://localhost:3000')
  document = Document(client)
  document.id = 'document-id'
  return document


@responses.activate
def test_state_preserves_document_attributes(document):
  state = {'id': document.id, 'state': 'pending', 'signing_groups': [{'stakeholders': []}]}
  responses.get(document.url('document-id/state'), json=state)
  assert document.get_state() == state
  assert document.get_data() == {'id': 'document-id'}


@responses.activate
@pytest.mark.parametrize('operation,method,status', [
  ('add_stakeholder', 'POST', 201), ('update_stakeholder', 'PUT', 200),
])
def test_stakeholder_payloads_and_results(document, operation, method, status):
  payload = {
    'email': 'reviewer@example.com', 'type': 'reviewer', 'name': 'José',
    'send_invite': False, 'allowed_signature_methods': ['FEA', 'FESCV'],
  }
  path = 'document-id/stakeholders'
  args = [payload]
  if operation == 'update_stakeholder':
    path += '/stakeholder-id'
    args.insert(0, 'stakeholder-id')
  result = {'id': 'stakeholder-id', **payload}
  responses.add(method, document.url(path), json=result, status=status)
  assert getattr(document, operation)(*args) == result
  request = responses.calls[0].request
  assert json.loads(request.body) == payload
  assert request.headers['Content-Type'] == 'application/json'
  assert document.id == 'document-id'


@responses.activate
@pytest.mark.parametrize('status', [204, 205])
def test_delete_stakeholder_preserves_empty_response_and_status(document, status):
  responses.delete(document.url('document-id/stakeholders/stakeholder-id'), status=status)
  response = document.delete_stakeholder('stakeholder-id')
  assert isinstance(response, requests.Response)
  assert response.status_code == status
  assert response.content == b''


@responses.activate
def test_zip_is_written_without_binary_changes(document, tmp_path):
  archive = io.BytesIO()
  with zipfile.ZipFile(archive, 'w') as zip_file:
    zip_file.writestr('signed.pdf', b'%PDF-1.4\n\x00\xff')
    zip_file.writestr('signature.xml', b'<signature/>')
  payload = archive.getvalue()
  responses.get(document.url('document-id/zip'), body=payload,
                content_type='application/zip')
  path = tmp_path / 'nested' / 'signed.zip'
  document.save_zip(path)
  assert path.read_bytes() == payload
  with zipfile.ZipFile(path) as zip_file:
    assert zip_file.testzip() is None


@responses.activate
@pytest.mark.parametrize('method,endpoint', [
  ('save_zip', 'zip'), ('save_file_signed', 'file_signed'), ('save_xml', 'xml'),
])
def test_failed_download_does_not_overwrite_existing_file(document, tmp_path, method, endpoint):
  path = tmp_path / 'existing'
  path.write_bytes(b'keep existing contents')
  responses.get(document.url(f'document-id/{endpoint}'), status=423)
  with pytest.raises(requests.HTTPError):
    getattr(document, method)(path)
  assert path.read_bytes() == b'keep existing contents'


@responses.activate
def test_xml_is_written_as_original_bytes(document, tmp_path):
  payload = '<?xml version="1.0" encoding="UTF-8"?><name>José</name>'.encode()
  responses.get(document.url('document-id/xml'), body=payload,
                content_type='application/xml')
  path = tmp_path / 'signature.xml'
  document.save_xml(path)
  assert path.read_bytes() == payload


@pytest.mark.parametrize('timeout', [None, 7])
def test_zip_uses_download_timeout(document, tmp_path, timeout):
  if timeout:
    document.client.set_timeout(timeout)
  with patch('mifiel.document.requests.get') as get:
    get.return_value.content = b'zip'
    document.save_zip(tmp_path / 'file.zip')
  assert get.call_args.kwargs['timeout'] == (timeout or 30)


@pytest.mark.parametrize('operation,args', [
  ('get_state', []), ('add_stakeholder', [{}]),
  ('update_stakeholder', ['stakeholder-id', {}]),
  ('delete_stakeholder', ['stakeholder-id']), ('save_zip', ['unused.zip']),
])
def test_document_id_required_before_network(document, operation, args):
  document.id = None
  with pytest.raises(ValueError, match='Document id'):
    getattr(document, operation)(*args)


@pytest.mark.parametrize('operation,args', [
  ('update_stakeholder', ['', {}]), ('delete_stakeholder', ['']),
])
def test_stakeholder_id_required_before_network(document, operation, args):
  with pytest.raises(ValueError, match='Stakeholder id'):
    getattr(document, operation)(*args)
