class Response(object):
  def __init__(self):
    object.__setattr__(self, 'datastore', {})

  def set_response(self, response):
    response.raise_for_status()
    object.__setattr__(self, 'datastore', response)

  def get_response(self):
    return self.datastore

  def __setattr__(self, name, value):
    self.set(name, value)

  def __getattr__(self, name):
    return self.get(name)

  def set(self, name, value):
    self.datastore[name] = value

  def get(self, name):
    return self.datastore[name]
