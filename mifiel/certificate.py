from mifiel import Base
import requests

class Document(Base):
  def __init__(self, mifiel):
    Base.__init__(self, mifiel, 'keys')
