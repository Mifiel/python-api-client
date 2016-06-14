"""
[ApiAuth](https://github.com/mgomes/api_auth) for python
Based on https://github.com/pd/httpie-api-auth by Kyle Hargraves
Usage:
import requests
requests.get(url, auth=ApiAuth(app_id, secret_key))

"""
from requests.auth import AuthBase

from .api_auth import ApiAuth

class RequestsApiAuth(AuthBase):
  def __init__(self, access_id, secret_key):
    self.auth = ApiAuth(access_id, secret_key)

  def __call__(self, request):
    return self.auth.sign(request)
