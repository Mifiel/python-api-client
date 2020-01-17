from mifiel import Base, Response
import mimetypes
from os.path import basename
import requests
try:
    import simplejson as json
except ImportError:
    import json

class Document(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'documents')

  @staticmethod
  def find(client, doc_id):
    doc = Document(client)
    doc.process_request('get', url=doc.url(doc_id))
    return doc

  @staticmethod
  def all(client):
    base = Document(client)
    response = base.execute_request('get', url=base.url())
    result = []
    for single in response.json():
      obj = Document(client)
      obj.set_data(single)
      result.append(obj)
    return result

  @staticmethod
  def create(client, signatories, file=None, dhash=None, callback_url=None, name=None):
    if not file and not dhash:
      raise ValueError('Either file or hash must be provided')
    if file and dhash:
      raise ValueError('Only one of file or hash must be provided')
    if dhash and not name:
      raise ValueError('A name is required when using hash')

    sig_numbers = {}

    for index, item in enumerate(signatories):
      for key, val in item.items():
        sig_numbers.update(
          {'signatories[' + str(index) + '][' + str(key) + ']': val}
        )

    data = sig_numbers

    if callback_url: data['callback_url'] = callback_url
    if file:
      mimetype = mimetypes.guess_type(file)[0]
      _file = open(file, 'rb')
      file = {'file': (basename(_file.name), _file, mimetype)}
    if dhash: data['original_hash'] = dhash
    if name: data['name'] = name

    doc = Document(client)
    doc.process_request('post', data=data, files=file)
    return doc

  def request_signature(self, signer, cc=None):
    path = '{}/{}'.format(self.id, 'request_signature')
    data = {
      'email': signer,
      'cc': cc
    }
    response = self.execute_request('post', url=self.url(path), json=data)
    return response.json()

  @staticmethod
  def delete(client, doc_id):
    base = Document(client)
    response = base.execute_request('delete', url=base.url(doc_id))
    try:
      return response.json()
    except json.JSONDecodeError:
      if response.status_code in [204, 205]:
        # if the response body is empty returns a dictionary with the success response
        return {'status': 'success'}
      else:
        return response.text

  @staticmethod
  def create_from_template(client, args={}):
    call = Base(client, 'templates')
    path = '{}/{}'.format(args['template_id'], 'generate_document')
    response = call.execute_request('post', url=call.url(path), json=args)
    doc = Document(client)
    doc.set_data(response)
    return doc

  @staticmethod
  def create_many_from_template(client, args={}):
    call = Base(client, 'templates')
    url = '{}/{}'.format(args['template_id'], 'generate_documents')
    response = call.execute_request('post', url=call.url(url), json=args)
    return response.json()

  def save_file(self, path):
    url_ = self.url('{}/file').format(self.id)
    response = requests.get(url_, auth=self.client.auth)
    with open(path, 'w') as file_:
      file_.write(response.text)

  def save_file_signed(self, path):
    url_ = self.url('{}/file_signed').format(self.id)
    response = requests.get(url_, auth=self.client.auth)
    with open(path, 'w') as file_:
      file_.write(response.text)

  def save_xml(self, path):
    url_ = self.url('{}/xml').format(self.id)
    response = requests.get(url_, auth=self.client.auth)
    with open(path, 'w') as file_:
      file_.write(response.text)
