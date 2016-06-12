"""
[ApiAuth](https://github.com/mgomes/api_auth) for python
Based on https://github.com/pd/httpie-api-auth by Kyle Hargraves
Usage:
import requests
requests.get(url, auth=ApiAuth(app_id, secret_key))

"""
import hmac, base64, hashlib, datetime
from requests.auth import AuthBase
from urllib.parse import urlparse

class ApiAuth(AuthBase):
  def __init__(self, access_id, secret_key):
    self.access_id = access_id
    self.secret_key = secret_key.encode('ascii')

  def __call__(self, request):
    method = request.method.upper()

    content_type = request.headers.get('content-type')
    if not content_type:
      content_type = ''

    content_md5 = request.headers.get('content-md5')
    if not content_md5:
      m = hashlib.md5()
      body = request.body
      if not body: body = ''
      m.update(body.encode('ascii'))
      content_md5 = base64.b64encode(m.digest()).decode()
      request.headers['content-md5'] = content_md5

    httpdate = request.headers.get('date')
    if not httpdate:
      now = datetime.datetime.utcnow()
      httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
      request.headers['Date'] = httpdate

    url  = urlparse(request.url)
    path = url.path
    if url.query:
      path = path + '?' + url.query

    canonical_string = '%s,%s,%s,%s,%s' % (method, content_type, content_md5, path, httpdate)

    digest = hmac.new(
      self.secret_key,
      canonical_string.encode('ascii'),
      hashlib.sha1
    ).digest()
    signature = base64.encodestring(digest).rstrip().decode()

    request.headers['Authorization'] = 'APIAuth %s:%s' % (self.access_id, signature)
    return request
