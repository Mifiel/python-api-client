from mifiel import Base
import mimetypes
import os
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
  def create(client, signatories, **kwargs):
    file = kwargs.get('file')
    dhash = kwargs.get('dhash')
    name = kwargs.get('name')
    if not file and not dhash:
      raise ValueError('Either file or hash must be provided')
    if file and dhash:
      raise ValueError('Only one of file or hash must be provided')
    if dhash and not name:
      raise ValueError('A name is required when using hash')

    data = kwargs.copy()
    data.pop('file', None)
    signatory_array_fields = []
    for index, item in enumerate(signatories):
      for key, val in item.items():
        if key == 'allowed_signature_methods' and isinstance(val, list):
          for method in val:
            signatory_array_fields.append(
              (f'signatories[{index}][{key}][]', method)
            )
        else:
          data[f'signatories[{index}][{key}]'] = val

    if 'viewers' in data:
      viewers = data.pop('viewers')
      for index, item in enumerate(viewers):
        for key, val in item.items():
          data.update(
            {'viewers[' + str(index) + '][' + str(key) + ']': val}
          )

    if 'callback_url' in kwargs:
      data['callback_url'] = kwargs.get('callback_url')
    if dhash:
      data['original_hash'] = data.pop('dhash')

    if signatory_array_fields:
      data = list(data.items()) + signatory_array_fields

    doc = Document(client)
    if file:
      mimetype = mimetypes.guess_type(str(file))[0]
      with open(file, 'rb') as upload:
        files = {'file': (basename(upload.name), upload, mimetype)}
        doc.process_request('post', data=data, files=files)
    else:
      doc.process_request('post', data=data)
    return doc

  def get_state(self):
    """Return document state, signing groups and stakeholders as a dictionary."""
    response = self.execute_request('get', url=self.url(self._document_path('state')))
    return response.json()

  def add_stakeholder(self, params):
    """Add a signer or reviewer and return the decoded API response."""
    response = self.execute_request(
      'post', url=self.url(self._document_path('stakeholders')), json=params,
    )
    return response.json()

  def update_stakeholder(self, stakeholder_id, params):
    """Update a stakeholder without replacing this document's attributes."""
    response = self.execute_request(
      'put', url=self.url(self._stakeholder_path(stakeholder_id)), json=params,
    )
    return response.json()

  def delete_stakeholder(self, stakeholder_id):
    """Return the HTTP response, including empty 204 or 205 responses."""
    return self.execute_request('delete', url=self.url(self._stakeholder_path(stakeholder_id)))

  def _document_path(self, operation):
    if not self.id:
      raise ValueError('Document id is required')
    return f'{self.id}/{operation}'

  def _stakeholder_path(self, stakeholder_id):
    if not stakeholder_id:
      raise ValueError('Stakeholder id is required')
    return self._document_path(f'stakeholders/{stakeholder_id}')

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
    self._save_download(path, 'file')

  def save_file_signed(self, path):
    self._save_download(path, 'file_signed')

  def save_zip(self, path):
    """Download the signed PDF/XML archive to a local file."""
    self._save_download(path, 'zip')

  def save_xml(self, path):
    self._save_download(path, 'xml')

  def _save_download(self, path, operation):
    url_ = self.url(self._document_path(operation))
    response = requests.get(url_, auth=self.client.auth, timeout=self._request_timeout())
    response.raise_for_status()
    self._ensure_parent_dir(path)
    with open(path, 'wb') as file_:
      file_.write(response.content)

  def _request_timeout(self):
    return self.client.timeout if self.client.timeout else 30

  @staticmethod
  def _ensure_parent_dir(path):
    directory = os.path.dirname(path)
    if directory:
      os.makedirs(directory, exist_ok=True)
