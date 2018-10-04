from mifiel import Base, Document
import mimetypes
from os.path import basename
import requests

class Template(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'templates')

  @staticmethod
  def find(client, template_id):
    template = Template(client)
    template.process_request('get', url=template.url(template_id))
    return template

  @staticmethod
  def all(client):
    base = Template(client)
    response = base.execute_request('get', url=base.url())
    result = []
    for single in response.json():
      obj = Template(client)
      obj.set_data(single)
      result.append(obj)
    return result

  @staticmethod
  def create(client, name, content, description=None, header=None, footer=None):
    template = Template(client)
    data = {
      'name': name,
      'description': description,
      'header': header,
      'content': content,
      'footer': footer
    }
    template.process_request('post', data=data)
    return template

  @staticmethod
  def delete(client, template_id):
    base = Template(client)
    response = base.execute_request('delete', url=base.url(template_id))
    return response.json()
