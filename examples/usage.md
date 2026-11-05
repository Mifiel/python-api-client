# Python API examples

These examples target the unreleased 2.1.0 SDK. The API contract is documented at
[docs.mifiel.com](https://docs.mifiel.com/en/).

## Configure a sandbox client

```python
import os

from mifiel import Client, Document, Query, Webhook

client = Client(os.environ['MIFIEL_APP_ID'], os.environ['MIFIEL_APP_SECRET'])
client.use_sandbox()
client.set_timeout(30)
```

## Create a document and read its state

```python
document = Document.create(
    client,
    [{'email': 'signer@example.com', 'allowed_signature_methods': ['FEA']}],
    file='contract.pdf',
    send_invites=False,
    remind_every=0,
)
state = document.get_state()
print(state['state'], state['signing_groups'])

# Work with an existing document without first fetching its legacy representation:
document = Document(client)
document.id = 'DOCUMENT_ID'
state = document.get_state()
```

## Manage document stakeholders

```python
reviewer = document.add_stakeholder({
    'email': 'reviewer@example.com',
    'name': 'Contract reviewer',
    'type': 'reviewer',
    'send_invite': False,
})
updated = document.update_stakeholder(reviewer['id'], {
    'email': reviewer['email'],
    'name': 'Updated reviewer',
    'type': 'reviewer',
    'send_invite': False,
})
response = document.delete_stakeholder(reviewer['id'])
print(response.status_code)  # 204 in the reference; 205 observed in sandbox.
```

State and stakeholder helpers return decoded dictionaries without replacing the
document's local attributes. Stakeholder deletion returns `requests.Response`,
including its status and any body. A deleted stakeholder may remain in document
state with `state: deleted`. Participation and document completion restrict edits.

## Download completed documents

```python
document.save_file_signed('downloads/signed.pdf')
document.save_xml('downloads/signature.xml')
document.save_zip('downloads/signed.zip')
```

These methods create parent directories and write original response bytes. They
use the client's timeout or a 30-second download timeout. Failed HTTP responses
raise before opening the destination file.

## Query records with pagination

```python
result = Query.execute(client, {
    'resource': 'document',
    'fields': 'id,file_name,created_at',
    'page': 1,
    'per_page': 25,
    'sort': 'created_at-desc',
    'version': '1.0.0',
})
records = result['records']
metadata = result.get('___metadata', {})
```

Queries use `/api/query` on the configured server. Other resource methods use
`/api/v1/`. All query response fields, including pagination metadata, pass through.

## Webhook subscriptions

```python
subscriptions = Webhook.all(client)
subscription = Webhook.create(client, 'https://example.com/callback', 'document_signed')

# This sends a real callback; invoke it only when the receiver is ready.
delivery = subscription.trigger(document.id, instant=False)
Webhook.delete(client, subscription.id)
```

Webhook support already exists in 2.0.0; 2.1.0 adds tests and consistent HTTP error
handling. Empty successful webhook deletions return `None`.

## Handle API errors

```python
import requests

try:
    state = document.get_state()
except requests.HTTPError as error:
    print('API request failed:', error.response.status_code)
```

All SDK HTTP methods now raise `requests.HTTPError` for unsuccessful HTTP responses.
Existing successful return values, including document/template objects and delete
results, are retained.
