from mifiel import Base


class Webhook(Base):
  """Account-level webhook subscriptions.

  See https://docs.mifiel.com/en/#tag/Webhooks
  """

  def __init__(self, client):
    Base.__init__(self, client, 'webhooks')

  @staticmethod
  def find(client, webhook_id):
    webhook = Webhook(client)
    webhook.process_request('get', url=webhook.url(webhook_id))
    return webhook

  @staticmethod
  def all(client):
    base = Webhook(client)
    response = base.execute_request('get', url=base.url())
    result = []
    for single in response.json():
      obj = Webhook(client)
      obj.set_data(single)
      result.append(obj)
    return result

  @staticmethod
  def create(client, url, callback_type):
    webhook = Webhook(client)
    webhook.process_request(
      'post',
      json={
        'url': url,
        'callback_type': callback_type,
      },
    )
    return webhook

  @staticmethod
  def delete(client, webhook_id):
    base = Webhook(client)
    response = base.execute_request('delete', url=base.url(webhook_id))
    if response.content:
      return response.json()
    return None

  def trigger(self, resource, instant=False):
    """Trigger delivery for this webhook.

    Args:
      resource: UUID of the related resource included in the callback payload.
      instant: When True, deliver immediately once instead of enqueueing retries.
    """
    if not self.id:
      raise ValueError('Webhook id is required to trigger')
    response = self.execute_request(
      'post',
      url=self.url('{}/trigger'.format(self.id)),
      json={
        'resource': resource,
        'instant': instant,
      },
    )
    if response.content:
      return response.json()
    return None
