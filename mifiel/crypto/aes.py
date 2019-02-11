import os
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES as AES_CIPHER
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class AES:
  ALGORITHM = AES_CIPHER.MODE_CBC

  @classmethod
  def encrypt(cls, password, data, iv):
    password, data, iv = cls.__validate_payload_bytes([password, data, iv])
    aes = AES_CIPHER.new(password, cls.ALGORITHM, iv)
    padded_data = pad(data, 16, style='pkcs7')
    ciphertext = aes.encrypt(padded_data)
    bytes_hex = hexlify(ciphertext)
    return bytes_hex.decode()

  @classmethod
  def decrypt(cls, password, encrypted_data, iv):
    password, encrypted_data, iv = cls.__validate_payload_bytes([password, encrypted_data, iv])
    try:
      encrypted_data = unhexlify(encrypted_data)
    except:
      pass
    aes = AES_CIPHER.new(password, cls.ALGORITHM, iv)
    decrypted_data = unpad(aes.decrypt(encrypted_data), 16)
    return decrypted_data.decode()

  @classmethod
  def random_iv(cls, length = 16):
    if length < 16:
      raise ValueError('IV lenght/size requested is too small, at least 16 is encouraged')
    return get_random_bytes(length)

  @staticmethod
  def __validate_payload_bytes(params):
    for i in range(len(params)):
      if isinstance(params[i], str):
        params[i] = str.encode(params[i])
    return params
