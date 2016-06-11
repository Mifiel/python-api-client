"""
[ApiAuth](https://github.com/mgomes/api_auth) for python

"""
import hmac, base64, hashlib, datetime

try:
  import urlparse
except ImportError:
  import urllib.parse

__version__ = '0.3.0'
__author__ = 'Kyle Hargraves'
__licence__ = 'MIT'

class ApiAuth:
  def __init__(self, access_id, secret_key):
    self.access_id = access_id
    self.secret_key = secret_key.encode('ascii')

  def sign_request(self, request):
    method = request.method.upper()

    content_type = request.headers.get('content-type')
    if not content_type:
      content_type = ''

    content_md5  = request.headers.get('content-md5')
    if not content_md5:
      content_md5 = ''

    httpdate = request.headers.get('date')
    if not httpdate:
      now = datetime.datetime.utcnow()
      httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
      request.headers['Date'] = httpdate

    path = ''
    # url  = urlparse.urlparse(request.url)
    # path = url.path
    # if url.query:
    #   path = path + '?' + url.query

    string_to_sign = '%s,%s,%s,%s,%s' % (method, content_type, content_md5, path, httpdate)
    digest = hmac.new(self.secret_key, string_to_sign, hashlib.sha1).digest()
    signature = base64.encodestring(digest).rstrip()

    request.headers['Authorization'] = 'APIAuth %s:%s' % (self.access_id, signature)
    return request
