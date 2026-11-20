from urllib.parse import urljoin

from .base import Base


class Query:
  """Advanced queries at /api/query, outside the versioned resource routes."""

  @staticmethod
  def execute(client, params):
    """Return the full decoded response, preserving records and pagination metadata."""
    if not params.get('resource') or not params.get('fields'):
      raise ValueError('Query resource and fields are required')
    response = Base(client, 'query').execute_request(
      'post', url=urljoin(client.url(), '/api/query'), json=params,
    )
    return response.json()
