# Mifiel Python API Client

[![Build Status][travis-image]][travis-url]
[![PyPI version][pypi-image]][pypi-url]

Python SDK for the [Mifiel](https://www.mifiel.com) API.

## Documentation

API reference, guides, and examples:

- English: https://docs.mifiel.com/en/
- Español: https://docs.mifiel.com/es/

This README covers installation and client setup only.

## Installation

```bash
pip install mifiel
```

## Setup

1. Create an account (production or [sandbox](https://app-sandbox.mifiel.com)).
2. Generate an `APP_ID` and `APP_SECRET` in [Access Tokens](https://app-sandbox.mifiel.com/settings/access-tokens).
3. Configure the client:

```python
from mifiel import Client

client = Client(app_id='APP_ID', secret_key='APP_SECRET')
# Production is the default (https://app.mifiel.com).
# For sandbox:
client.use_sandbox()
# Or override the base URL:
# client.set_base_url('https://app-sandbox.mifiel.com')
```

## Development

This project uses [Poetry](https://python-poetry.org/docs/#installation):

```bash
poetry install
poetry run pytest
```

## Contributing

1. Fork it (https://github.com/Mifiel/python-api-client/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

[travis-image]: https://travis-ci.org/Mifiel/python-api-client.svg?branch=master
[travis-url]: https://travis-ci.org/Mifiel/python-api-client
[pypi-image]: https://badge.fury.io/py/mifiel.svg
[pypi-url]: https://badge.fury.io/py/mifiel
