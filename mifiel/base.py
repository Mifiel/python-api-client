from mifiel import Response
import requests

class Base(object):
  def __init__(self, client, path):
    object.__setattr__(self, 'sandbox', False)
    object.__setattr__(self, 'path', path)
    object.__setattr__(self, 'client', client)
    object.__setattr__(self, 'response', Response())
    # initialize id
    self.id = None

  def save(self):
    if self.id is None:
      return False
    self.process_request('put', url=self.url(self.id), data=self.get_data())

  def url(self, path=None):
    p = self.path
    if path:
      p = '{}/{}'.format(p, path)

    return self.client.url().format(path=p)

  def execute_request(self, method, url=None, data=None, json=None, files=None, params=None):
    if method not in ('post', 'put', 'get', 'delete'):
      raise ValueError(f'Unsupported HTTP method: {method}')
    if not url:
      url = self.url()

    kwargs = dict(
      url=url,
      auth=self.client.auth,
      json=json,
    )
    if params is not None:
      kwargs['params'] = params
    if self.client.timeout:
      kwargs.update({
        'timeout': self.client.timeout
      })

    if method in ('post', 'put'):
      kwargs.update({
        'data': self._form_data(data),
        'files': files
      })

    try:
      response = getattr(requests, method)(**kwargs)
      response.raise_for_status()
      return response
    finally:
      # Close uploads even when the request or HTTP status validation fails.
      if files and method in ('post', 'put'):
        parts = files.values() if isinstance(files, dict) else (part for _, part in files)
        for part in parts:
          stream = part[1] if isinstance(part, (tuple, list)) else part
          if hasattr(stream, 'close'):
            stream.close()

  @staticmethod
  def _form_data(data):
    # Requests otherwise serializes booleans as "False"/"True", which are not
    # canonical boolean values for the API's form parameters.
    if isinstance(data, dict):
      data = data.items()
    elif not isinstance(data, (list, tuple)):
      return data
    return [(key, str(value).lower() if isinstance(value, bool) else value)
            for key, value in data]

  def process_request(self, method, url=None, data=None, json=None, files=None, params=None):
    response = self.execute_request(method, url, data, json, files, params)
    self.set_data(response)

  def set_data(self, response):
    self.response.set_response(response)

  def get_data(self):
    return self.response.get_response()

  def __setattr__(self, name, value):
    self.response.set(name, value)

  def __getattr__(self, name):
    return self.response.get(name)
