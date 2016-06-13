from mifiel import ApiAuth

class Client:
  def __init__(self, app_id, secret_key):
    self.sandbox = False
    self.auth = ApiAuth(app_id, secret_key)
    self.base_url = 'https://www.mifiel.com'

  def use_sandbox(self):
    self.sandbox = True
    self.base_url = 'https://sandbox.mifiel.com'

  def set_base_url(self, base_url):
    self.base_url = base_url

  def url(self):
    return self.base_url + '/api/v1/{path}'
