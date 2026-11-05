import json

import pytest
import requests
import responses

from mifiel import Client, Webhook


@pytest.fixture
def client():
  client = Client('test-app-id', 'test-secret')
  client.set_base_url('http://localhost:3000')
  return client


@responses.activate
def test_create_and_list_webhooks(client):
  payload = {'url': 'https://example.com/callback', 'callback_type': 'document_signed'}
  result = {'id': 'webhook-id', **payload}
  responses.post(Webhook(client).url(), json=result, status=201)
  responses.get(Webhook(client).url(), json=[result])
  webhook = Webhook.create(client, **payload)
  assert webhook.id == 'webhook-id'
  assert json.loads(responses.calls[0].request.body) == payload
  assert [hook.id for hook in Webhook.all(client)] == ['webhook-id']


@responses.activate
@pytest.mark.parametrize('instant,status,result', [
  (False, 202, {'status': 'queued'}), (True, 200, {'status': 'sent'}),
])
def test_trigger_preserves_instant_flag(client, instant, status, result):
  webhook = Webhook(client)
  webhook.id = 'webhook-id'
  responses.post(webhook.url('webhook-id/trigger'), json=result, status=status)
  assert webhook.trigger('document-id', instant=instant) == result
  assert json.loads(responses.calls[0].request.body) == {
    'resource': 'document-id', 'instant': instant,
  }


@responses.activate
@pytest.mark.parametrize('status', [204, 205])
def test_delete_empty_response(client, status):
  responses.delete(Webhook(client).url('webhook-id'), status=status)
  assert Webhook.delete(client, 'webhook-id') is None


@responses.activate
def test_delete_error_raises(client):
  responses.delete(Webhook(client).url('webhook-id'), json={'error': 'denied'}, status=403)
  with pytest.raises(requests.HTTPError):
    Webhook.delete(client, 'webhook-id')
