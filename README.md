# Mifiel Python Library

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

To start using the API in the Sandbox environment you need to first create an account at [app-sandbox.mifiel.com](https://app-sandbox.mifiel.com).

Once you have an account you will need an APP_ID and an APP_SECRET which you can generate in [app-sandbox.mifiel.com/settings/access-tokens](https://app-sandbox.mifiel.com/settings/access-tokens).

By default the client talks to production (`https://app.mifiel.com`). For sandbox, call `client.use_sandbox()` (uses `https://app-sandbox.mifiel.com`), or override with `client.set_base_url(...)`.

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
doc = Document.create(client, signatories, file='test/fixtures/example.pdf')

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

Just clone the repo, install dependencies as you would in development and run:

```bash
poetry run pytest
```

## Publish

The package is published to [PyPI](https://pypi.org/project/mifiel/) as `mifiel` using Poetry. Bump the version in `pyproject.toml` (and `CHANGELOG.md`) first — PyPI will reject a version that already exists.

Create an [API token](https://pypi.org/manage/account/token/) on PyPI (you need Maintainer or Owner on the project), then configure Poetry:

```bash
poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmc...
```

Or set it for a single session:

```bash
export POETRY_PYPI_TOKEN_PYPI=pypi-AgEIcHlwaS5vcmc...
```

Build and publish:

```bash
poetry install --no-interaction
poetry run pytest
poetry publish --build
```

To dry-run against [TestPyPI](https://test.pypi.org/):

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-...
poetry publish --repository testpypi --build
```

## Contributing

1. Fork it ( https://github.com/Mifiel/python-api-client/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

[travis-image]: https://travis-ci.org/Mifiel/python-api-client.svg?branch=master
[travis-url]: https://travis-ci.org/Mifiel/python-api-client
[pypi-image]: https://badge.fury.io/py/mifiel.svg
[pypi-url]: https://badge.fury.io/py/mifiel
