import hmac
import base64
import hashlib
import datetime
try:
  from urllib.parse import urlparse
except:
  from urlparse import urlparse

class Signature:
  def __init__(self, secret_key):
    self.secret_key = secret_key.encode('ascii')

  def build(self, method, url, body, content_md5=None, content_type=None, httpdate=None):
    method = method.upper()

    if not content_type:
      content_type = ''

    self.content_md5 = content_md5
    if not self.content_md5:
      m = hashlib.md5()
      if not body:
        body = ''
      if isinstance(body, str):
        try:
          m.update(body.encode('ascii'))
        # For Python 2.7
        except(UnicodeDecodeError):
          m.update(body)
      else:
        m.update(body)

      self.content_md5 = base64.b64encode(m.digest()).decode()

    self.httpdate = httpdate
    if not self.httpdate:
      now = datetime.datetime.utcnow()
      self.httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

    url = urlparse(url)
    path = url.path
    if url.query:
      path = path + '?' + url.query

    rep = (method, content_type, self.content_md5, path, self.httpdate)
    self.canonical_string = '%s,%s,%s,%s,%s' % rep

    digest = hmac.new(
      self.secret_key,
      self.canonical_string.encode('ascii'),
      hashlib.sha1
    ).digest()
    self.signature = base64.b64encode(digest).rstrip().decode()
