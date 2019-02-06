import os
import binascii
from Crypto.Cipher import AES as AES_CIPHER
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class AES:
  ALGORITHM = AES_CIPHER.MODE_CBC
  DEFAULT_BLOCK_SIZE = 16

  @classmethod
  def encrypt(cls, password, data, iv):
    password, data, iv = cls.__validate_payload_bytes([password, data, iv])
    aes = AES_CIPHER.new(password, cls.ALGORITHM, iv)
    padded_data = pad(data, cls.DEFAULT_BLOCK_SIZE, style='pkcs7')
    cipher_text = aes.encrypt(padded_data)
    bytes_hex = binascii.hexlify(cipher_text)
    return bytes_hex.decode('utf-8')

  @classmethod
  def decrypt(cls, password, encrypted_data, iv):
    password, encrypted_data, iv = cls.__validate_payload_bytes([password, encrypted_data, iv])
    data_bytes = binascii.unhexlify(encrypted_data)
    aes = AES_CIPHER.new(password, cls.ALGORITHM, iv)
    decrypted_data = unpad(aes.decrypt(data_bytes), cls.DEFAULT_BLOCK_SIZE)
    return decrypted_data.decode('utf-8')

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
