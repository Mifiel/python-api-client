from mifiel import ApiAuth

class Client:
  def __init__(self, app_id, secret_key):
    self.sandbox = False
    self.auth = ApiAuth(app_id, secret_key)

  def use_sandbox(self):
    self.sandbox = True

  def url(self):
    if self.sandbox:
      return 'https://sandbox.mifiel.com/api/v1/{path}'
    return 'https://www.mifiel.com/api/v1/{path}'
