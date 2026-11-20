import json

import pytest
import requests
import responses

import mifiel


@responses.activate
@pytest.mark.parametrize('server', [
  'https://app.mifiel.com', 'https://app-sandbox.mifiel.com', 'http://localhost:3000',
])
def test_query_uses_unversioned_route_and_preserves_metadata(server):
  client = mifiel.Client('test-app-id', 'test-secret')
  client.set_base_url(server)
  params = {'resource': 'document', 'fields': 'id,file_name', 'page': 2, 'per_page': 1,
            'q': {'file_name': {'eq': 'Contrato.pdf'}}, 'version': '1.0.0'}
  result = {'records': [{'id': 'document-id'}],
            '___metadata': {'page': 2, 'total_count': 3, 'page_count': 3}}
  responses.post(server + '/api/query', json=result)
  assert mifiel.Query.execute(client, params) == result
  request = responses.calls[0].request
  assert json.loads(request.body) == params
  assert request.headers['Authorization'].startswith('APIAuth test-app-id:')


@pytest.mark.parametrize('params', [{}, {'resource': 'document'}, {'fields': 'id'},
                                   {'resource': '', 'fields': 'id'}])
def test_query_requires_resource_and_fields(params):
  with pytest.raises(ValueError, match='resource and fields'):
    mifiel.Query.execute(mifiel.Client('test-app-id', 'test-secret'), params)


@responses.activate
def test_query_raises_http_errors():
  client = mifiel.Client('test-app-id', 'test-secret')
  client.use_sandbox()
  responses.post('https://app-sandbox.mifiel.com/api/query', status=400)
  with pytest.raises(requests.HTTPError):
    mifiel.Query.execute(client, {'resource': 'document', 'fields': 'id'})
