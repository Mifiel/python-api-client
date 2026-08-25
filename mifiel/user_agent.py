import platform

import requests

from mifiel.version import __version__


def build_user_agent():
  """Build a User-Agent matching other Mifiel API clients.

  Example: PYTHON/3.12.1 mifiel/2.0.0 requests/2.32.5 (Linux/6.8.0)
  """
  return ' '.join([
    f'PYTHON/{platform.python_version()}',
    f'mifiel/{__version__}',
    f'requests/{requests.__version__}',
    f'({platform.system().replace(" ", "_")}/{platform.release().replace(" ", "_")})',
  ])
