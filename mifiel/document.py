from mifiel import Base

class Document(Base):
  def __init__(self, mifiel):
    Base.__init__(self, mifiel, 'documents')
