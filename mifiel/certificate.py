from mifiel import Base

class Document(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'keys')
