# Mifiel Python Library

[![Coverage Status][coveralls-image]][coveralls-url]
[![Build Status][travis-image]][travis-url]
[![PyPI version][pypi-image]][pypi-url]

Python library for [Mifiel](https://www.mifiel.com) API.
Please read our [documentation](http://docs.mifiel.com) for instructions on how to start using the API.

## Installation

```bash
pip install mifiel
```

## Usage

For your convenience Mifiel offers a Sandbox environment where you can confidently test your code.

To start using the API in the Sandbox environment you need to first create an account at [sandbox.mifiel.com](https://sandbox.mifiel.com).

Once you have an account you will need an APP_ID and an APP_SECRET which you can generate in [sandbox.mifiel.com/access_tokens](https://sandbox.mifiel.com/access_tokens).

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

- Save Document related files

```python
from mifiel import Document, Client
client = Client(app_id='APP_ID', secret_key='APP_SECRET')

doc = Document.find(client, 'id')
# save the original file
doc.save_file('path/to/save/file.pdf')
# save the signed file (original file + signatures page)
doc.save_file_signed('path/to/save/file-signed.pdf')
# save the signed xml file
doc.save_xml('path/to/save/xml.xml')
```

## Development

### Install dependencies

This project uses [poetry](https://python-poetry.org/) which you can install [here](https://python-poetry.org/docs/#installation), the just run `install` command:

```bash
poetry install
```

## Test

Just clone the repo, install dependencies as you would in development and run `nose2` or `poetry run nose2`

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
