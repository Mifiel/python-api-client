# Mifiel Python Library

[![Coverage Status][coveralls-image]][coveralls-url]
[![Build Status][travis-image]][travis-url]
[![PyPI version][pypi-image]][pypi-url]

Pyton library for [Mifiel](https://www.mifiel.com) API.
Please read our [documentation](http://docs.mifiel.com) for instructions on how to start using the API.

## Installation

```bash
pip install mifiel
```

## Usage

To start using the API you will need an APP_ID and a APP_SECRET which will be provided upon request (contact us at hola@mifiel.com).

You will first need to create an account in [mifiel.com](https://www.mifiel.com) since the APP_ID and APP_SECRET will be linked to your account.

### Document methods:

For now, the only methods available are **find** and **create**. Contributions are greatly appreciated.

- Find:

```python
from mifiel import Document, Client
client = Client(app_id='APP_ID', secret_key='APP_SECRET')

doc = Document.find(client, 'id')
document.original_hash
document.file
document.file_signed
# ...
```

- Create:

```python
from mifiel import Document, Client
client = Client(app_id='APP_ID', secret_key='APP_SECRET')

signatories = [
  { 
    'name': 'Signer 1', 
    'email': 'signer1@email.com', 
    'tax_id': 'AAA010101AAA' 
  },
  { 
    'name': 'Signer 2', 
    'email': 
    'signer2@email.com', 
    'tax_id': 'AAA010102AAA'
  }
]
# Providde the SHA256 hash of the file you want to sign.
doc = Document.create(client, signatories, dhash='some-sha256-hash')
# Or just send the file and we'll take care of everything.
# We will store the file for you. 
doc = Document.create(client, signatories, file='test/fixtures/example.pdf')

doc.id # -> '7500e528-ac6f-4ad3-9afd-74487c11576a'
doc.id # -> '7500e528-ac6f-4ad3-9afd-74487c11576a'
```

## Development

### Install dependencies

```bash
pip install -r requirements.txt
```

## Test

Just clone the repo, install dependencies as you would in development and run `nose2` or `python setup.py test`

## Contributing

1. Fork it ( https://github.com/Mifiel/python-api-client/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

[coveralls-image]: https://coveralls.io/repos/github/Mifiel/python-api-client/badge.svg?branch=master
[coveralls-url]: https://coveralls.io/github/Mifiel/python-api-client?branch=master

[travis-image]: https://travis-ci.org/Mifiel/python-api-client.svg?branch=master
[travis-url]: https://travis-ci.org/Mifiel/python-api-client

[pypi-image]: https://badge.fury.io/py/mifiel.svg
[pypi-url]: https://badge.fury.io/py/mifiel
