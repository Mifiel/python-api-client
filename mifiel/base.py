from mifiel import Response
import requests

class Base(object):
  def __init__(self, mifiel, path):
    object.__setattr__(self, 'sandbox', False)
    object.__setattr__(self, 'path', path)
    object.__setattr__(self, 'mifiel', mifiel)
    object.__setattr__(self, 'response', Response())

  def save(self):
    if self.id:
      self.process_request('put', url=self.url(self.id), data=self.get_data())
    else:
      self.process_request('post', data=self.get_data())

  def url(self, path=None):
    p = self.path
    if path:
      p = '{}/{}'.format(p, path)

    return self.mifiel.url().format(path=p)

  def process_request(self, method, url=None, data=None):
    if not url:
      url = self.url()

    if method == 'post':
      response = requests.post(url, auth=self.mifiel.auth, json=data)
    elif method == 'put':
      response = requests.put(url, auth=self.mifiel.auth, json=data)
    elif method == 'get':
      response = requests.get(url, auth=self.mifiel.auth, json=data)
    elif method == 'delete':
      response = requests.delete(url, auth=self.mifiel.auth, json=data)

    self.set_data(response)

  def set_data(self, response):
    self.response.set_response(response)

  def get_data(self):
    return self.response.get_response()

  def __setattr__(self, name, value):
    self.response.set(name, value)

  def __getattr__(self, name):
    return self.response.get(name)
