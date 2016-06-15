"""
[ApiAuth](https://github.com/mgomes/api_auth) for python

"""

from .signature import Signature

class ApiAuth():
  def __init__(self, access_id, secret_key):
    self.access_id = access_id
    self.secret_key = secret_key

  def sign(self, request):
    sig = Signature(self.secret_key)
    sig.build(
      method=request.method,
      url=request.url,
      body=request.body,
      content_md5=request.headers.get('content-md5'),
      content_type=request.headers.get('content-type'),
      httpdate=request.headers.get('date')
    )

    request.headers['content-md5'] = sig.content_md5
    request.headers['date'] = sig.httpdate

    auth = 'APIAuth %s:%s' % (self.access_id, sig.signature)
    request.headers['Authorization'] = auth
    return request
