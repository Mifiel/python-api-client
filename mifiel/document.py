from mifiel import Base

class Document(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'documents')

  @staticmethod
  def get(client, doc_id):
    doc = Document(client)
    doc.process_request('get', url=doc.url(doc_id))
    return doc

  @staticmethod
  def create(client, signatories, file=None, dhash=None, callback_url=None):
    if not file and not dhash:
      raise ValueError('Either file or hash must be provided')
    if file and dhash:
      raise ValueError('Only one of file or hash must be provided')

    data = { 'signatories': signatories }
    if callback_url: data['callback_url'] = callback_url
    if file: data['file'] = open(file)
    if dhash: data['original_hash'] = dhash

    doc = Document(client)
    doc.process_request('post', data=data)
    return doc
