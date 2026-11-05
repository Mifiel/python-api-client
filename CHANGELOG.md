# Changelog #

## v2.1.0 - Unreleased

### Features

- Add `Document.get_state()`, `add_stakeholder()`, `update_stakeholder()` and
  `delete_stakeholder()` for document state and signer/reviewer management.
- Add `Document.save_zip()` for signed PDF/XML archives.
- Export `Query.execute(client, params)` for advanced queries at `/api/query`,
  preserving the entire response and pagination metadata.
- Add Python examples, webhook coverage and CI coverage through Python 3.14.

### Bug fixes

- Send form data on PUT requests so document and template updates persist changes.
- Encode form booleans as lowercase `true`/`false`; retain zero and empty values.
- Support GET query parameters through `params`.
- Raise `requests.HTTPError` for failed API requests, including lists, deletes and
  webhook operations that previously returned error payloads as successful results.
- Close uploads on request failure and omit the local file path from upload form data.
- Save XML as original response bytes and check document IDs before downloads.

### Compatibility

- Python >=3.10 and Requests 2.x requirements are unchanged.
- `delete_stakeholder()` returns the HTTP response so callers can inspect empty
  204 responses (documented) or 205 responses (observed in sandbox).
- Existing successful return values remain unchanged; callers should handle
  `requests.HTTPError` for unsuccessful HTTP responses.

## v2.0.0 - 21.Aug.2026

### Breaking changes

- **Default API hosts** now use the canonical app domains:
  - Production: `https://www.mifiel.com` → `https://app.mifiel.com`
  - Sandbox (`Client.use_sandbox()`): `https://sandbox.mifiel.com` → `https://app-sandbox.mifiel.com`
- If you relied on the previous defaults (or on mocks/stubs keyed to those hosts), update your configuration or call `set_base_url(...)` explicitly.

### Features

- Send a standardized `User-Agent` on API requests, e.g. `PYTHON/3.12.1 mifiel/2.0.0 requests/2.32.5 (Linux/6.8.0)`.

### Migration

```python
from mifiel import Client

client = Client(app_id='APP_ID', secret_key='APP_SECRET')
# Production requests now go to https://app.mifiel.com/api/v1/...

client.use_sandbox()
# Sandbox requests now go to https://app-sandbox.mifiel.com/api/v1/...
```

## v1.0.0 - 22.Apr.2026

### Breaking changes

- **Python**: the minimum supported version is now **3.10** (Python **3.9** is no longer supported). This release is tagged **1.0.0** to reflect that compatibility change — [PR#16](https://github.com/Mifiel/python-api-client/pull/16)

### Bug fixes

- Encode `allowed_signature_methods` correctly when creating documents — [PR#15](https://github.com/Mifiel/python-api-client/pull/15)

### Tooling

- Modernize packaging and CI (Poetry-only build, pytest, Ruff, upgraded dependencies, Travis on Python 3.10–3.12, remove legacy `setup.py` / `requirements.txt` install path) — [PR#16](https://github.com/Mifiel/python-api-client/pull/16)

## v0.0.11 - 23.Sep.2020 ##
### Features
- Allow to add viewers on document creation

## v0.0.10 - 2.Sep.2020
### Features
- Allow to pass any argument to Document.create to support more features

## v0.0.9 - 28.Ago.2020
### Bug fixes
- Fix save_file and save_file_signed to save binary files

## v0.0.8 - 22.Jun.2020
### Features
- Ability to use the timeout parameter of the requests

## v0.0.7 - 17.Jan.2020
### Bug fixes
- Allow empty responses from server (status codes 204 and 205) - [PR#8](https://github.com/Mifiel/python-api-client/pull/8)

## v0.0.6 - 7.Nov.2019
### Bug fixes
- Fix authentication when the system locale is different than en_US - [PR#6](https://github.com/Mifiel/python-api-client/pull/6)
