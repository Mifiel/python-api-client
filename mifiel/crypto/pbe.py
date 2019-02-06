import re
import binascii
from Crypto.Hash import SHA256, SHA, HMAC
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

class PBE:
  DEFAULT_DIGEST = SHA256
  MIN_ITERATIONS = 1000
  MAX_ITERATIONS = 99999
  MAX_KEY_LENGTH = 1000
  MIN_SALT_LENGTH = 16

  @classmethod
  def random_password(cls, length = 32):
    password = b''
    while len(password) < length:
      password += re.sub(b'[^\x20-\x7E]', b'', get_random_bytes(100))
    return password.decode()[0:length]

  @classmethod
  def random_salt(cls, size = 16):
    if size < cls.MIN_SALT_LENGTH:
      raise ValueError('PBE.random_salt size too short, minimum required 16 (default)')
    return get_random_bytes(size)

  @classmethod
  def get_derived_key(cls, password, size=32, salt='', iterations=1000):
    if iterations < cls.MIN_ITERATIONS:
      raise ValueError('PBE.get_derived_key number of iterations too low')
    if iterations > cls.MAX_ITERATIONS:
      raise ValueError('PBE.get_derived_key number of iterations too high')
    if size > cls.MAX_KEY_LENGTH:
      raise ValueError('PBE.get_derived_key size requested for key, too high')
    key = PBKDF2(password, salt, dkLen=size, count=iterations, prf=lambda p,s: HMAC.new(p,s,cls.DEFAULT_DIGEST).digest())
    key_bytes = binascii.hexlify(key)
    return key_bytes.decode('utf-8')
