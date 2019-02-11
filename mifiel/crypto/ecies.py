from binascii import hexlify, unhexlify
from Crypto.Hash import SHA256, SHA512, HMAC
from Crypto.Cipher import AES as AES_CIPHER
from Crypto.Random import get_random_bytes
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad, unpad
from coincurve import PrivateKey, PublicKey

class ECIES:
  HMAC_DIGEST = SHA256
  KDF_DIGEST = SHA512
  IV_SIZE = 16
  CIPHER = AES_CIPHER.MODE_CBC

  @classmethod
  def encrypt(cls, pub_key_hex, message):
    public_key = PublicKey(unhexlify(pub_key_hex))
    ephemeral_key = PrivateKey()
    derived_key = cls.__ecdh(ephemeral_key, public_key)
    cipher_key, hmac_key = cls.__gen_cipher_hmac_keys(derived_key)
    return cls.__gen_encrypted_message(message, ephemeral_key, cipher_key, hmac_key)

  @classmethod
  def decrypt(cls, priv_key_hex, encrypted_message):
    iv, ephemeral_pub_hex, ciphertext, mac = cls.__parse_encrypted_message(encrypted_message)
    private_key = PrivateKey.from_hex(priv_key_hex)
    ephemeral_pub_key = PublicKey(unhexlify(ephemeral_pub_hex))
    derived_key = cls.__ecdh(private_key, ephemeral_pub_key)
    cipher_key, hmac_key = cls.__gen_cipher_hmac_keys(derived_key)
    partial = iv + ephemeral_pub_hex + ciphertext
    computed_mac = cls.__compute_hmac(hmac_key, unhexlify(partial))
    if computed_mac != mac:
      raise ValueError('Invalid mac')
    cihpertext_bytes = unhexlify(ciphertext)
    cipher = AES_CIPHER.new(cipher_key, cls.CIPHER, unhexlify(iv))
    decrypted_msg = unpad(cipher.decrypt(cihpertext_bytes), 16)
    return decrypted_msg.decode()

  # NOTE: WHY USE THIS METHOD INSTEAD OF coincurve.PrivateKey.ecdh?
  # coincurve.PrivateKey.ecdh returns the secret (x point) hashed with SHA256
  # What we need is the plain secret int (x point) to be hashed with SHA512 (SHA512 being our KDF)
  @classmethod
  def __ecdh(cls, private_key, public_key):
    shared_secret, __ = public_key.multiply(private_key.secret).point()
    x_point_bytes = long_to_bytes(shared_secret)
    kdf = cls.KDF_DIGEST.new(x_point_bytes)
    derived_key = kdf.hexdigest()
    return derived_key

  @classmethod
  def __gen_cipher_hmac_keys(cls, derived_key):
    cipher_key = derived_key[0:SHA256.block_size]
    hmac_key = derived_key[SHA256.block_size:]
    return (unhexlify(cipher_key), unhexlify(hmac_key))

  @classmethod
  def __compute_hmac(cls, key, data):
    hmac_digest = HMAC.new(key, digestmod=cls.HMAC_DIGEST).update(data)
    return hmac_digest.hexdigest()

  @classmethod
  def __gen_encrypted_message(cls, message, ephemeral_key, cipher_key, hmac_key):
    iv = get_random_bytes(cls.IV_SIZE)
    cipher = AES_CIPHER.new(cipher_key, cls.CIPHER, iv)
    padded_msg = pad(str.encode(message), 16, style='pkcs7')
    ciphertext = cipher.encrypt(padded_msg)
    partial = iv + ephemeral_key.public_key.format() + ciphertext
    mac = cls.__compute_hmac(hmac_key, partial)
    return hexlify(partial).decode() + mac

  @classmethod
  def __parse_encrypted_message(cls, encrypted_message):
    msg_len = len(encrypted_message)
    iv_hex_len = cls.IV_SIZE * 2
    ephem_pub_prefix = encrypted_message[iv_hex_len:iv_hex_len + 2]
    ephem_pub_key_len = 130 if ephem_pub_prefix == '04' else 66 # compressed 66, uncompressed 130
    ciphertext_len = msg_len - ephem_pub_key_len - SHA256.block_size - iv_hex_len
    if ciphertext_len < 1:
      raise ValueError('Encrypted message too short')
    iv = encrypted_message[0:iv_hex_len]
    ephem_pub_key = encrypted_message[iv_hex_len:iv_hex_len + ephem_pub_key_len]
    ciphertext = encrypted_message[iv_hex_len + ephem_pub_key_len:-SHA256.block_size]
    mac = encrypted_message[msg_len - SHA256.block_size:]
    return (iv, ephem_pub_key, ciphertext, mac)
