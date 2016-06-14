from mifiel import Base

class Certificate(Base):
  def __init__(self, client):
    Base.__init__(self, client, 'keys')
