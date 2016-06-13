from mifiel import Base
import requests

class Document(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'keys')
