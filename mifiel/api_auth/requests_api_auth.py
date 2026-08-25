"""
[ApiAuth](https://github.com/mgomes/api_auth) for python
Based on https://github.com/pd/httpie-api-auth by Kyle Hargraves
Usage:
import requests
requests.get(url, auth=ApiAuth(app_id, secret_key))

"""
from requests.auth import AuthBase

from .api_auth import ApiAuth
from mifiel.user_agent import build_user_agent

class RequestsApiAuth(AuthBase):
  def __init__(self, access_id, secret_key):
    self.auth = ApiAuth(access_id, secret_key)

  def __call__(self, request):
    request.headers['User-Agent'] = build_user_agent()
    return self.auth.sign(request)
