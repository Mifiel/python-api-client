from mifiel import Base

class Document(Base):
  def __init__(self, mifiel):
    Base.__init__(self, mifiel, 'documents')

  @staticmethod
  def get(mifiel, doc_id):
    doc = Document(mifiel)
    doc.process_request('get', url=doc.url(doc_id))
    return doc

  @staticmethod
  def create(mifiel, signatories, file=None, dhash=None, callback_url=None):
    if not file and not dhash:
      raise ValueError('Either file or hash must be provided')
    if file and dhash:
      raise ValueError('Only one of file or hash must be provided')

    data = { 'signatories': signatories }
    if callback_url: data['callback_url'] = callback_url
    if file: data['file'] = open(file)
    if dhash: data['original_hash'] = dhash

    doc = Document(mifiel)
    doc.process_request('post', data=data)
    return doc
