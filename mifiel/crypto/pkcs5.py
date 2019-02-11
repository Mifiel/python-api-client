from binascii import hexlify, unhexlify
from asn1crypto.core import Sequence, ObjectIdentifier, OctetString, Integer
from .pbe import PBE
from .aes import AES


class PKCS5:
  PKCS5_OID = '1.2.840.113549.1.5.13'
  PBKDF2_OID = '1.2.840.113549.1.5.12'
  HMAC_SHA256_OID = '1.2.840.113549.2.9'
  AES_128_CBC_OID = '2.16.840.1.101.3.4.1.2'
  AES_192_CBC_OID = '2.16.840.1.101.3.4.1.22'
  AES_256_CBC_OID = '2.16.840.1.101.3.4.1.42'

  def __init__(self, asn1_source=None):
    if asn1_source is not None:
      self.load_asn1(asn1_source)

  def decrypt_data(self, password):
    key_size = self.__key_size_bytes()
    derived_key = PBE.get_derived_key(password, size=key_size, salt=self.salt, iterations=self.iterations)
    return AES.decrypt(unhexlify(derived_key), self.cipher_data, self.iv)

  def dump_asn1(self):
    hmac_alg = AlgSequence()
    hmac_alg['0'] = self.HMAC_SHA256_OID
    kdf_info = KDFInfoSequence()
    kdf_info['0'] = OctetString(self.salt)
    kdf_info['1'] = Integer(self.iterations)
    kdf_info['2'] = hmac_alg
    pk_info = PKInfoSequence()
    pk_info['0'] = ObjectIdentifier(self.PBKDF2_OID)
    pk_info['1'] = kdf_info
    iv_key_size = IVKeySizeSequence()
    iv_key_size['0'] = ObjectIdentifier(self.key_size)
    iv_key_size['1'] = OctetString(self.iv)
    pbkdf2 = PBKDF2Sequence()
    pbkdf2['0'] = pk_info
    pbkdf2['1'] = iv_key_size
    pbes2 = PBES2Sequence()
    pbes2['0'] = ObjectIdentifier(self.PKCS5_OID)
    pbes2['1'] = pbkdf2
    pkcs5 = PKCS5Sequence()
    pkcs5['0'] = pbes2
    pkcs5['1'] = OctetString(self.cipher_data)
    return hexlify(pkcs5.dump()).decode()

  def load_asn1(self, asn1_source):
    if type(asn1_source) is str:
      self.__load_asn1_by_hex(asn1_source)
    elif type(asn1_source) is dict:
      self.__load_asn1_by_dict(asn1_source)
    else:
      raise ValueError('ASN.1 input format provided not supported.')

  def __load_asn1_by_dict(self, asn1_dict):
    asn1_params = ('iv', 'salt', 'iterations', 'key_size', 'cipher_data')
    try:
      iv, salt, iterations, key_size, cipher_data = [asn1_dict[k] for k in asn1_params]
      self.iv = unhexlify(iv) if type(iv) is str else iv
      self.salt = unhexlify(salt) if type(salt) is str else salt
      self.iterations = iterations
      self.key_size = key_size
      self.cipher_data = unhexlify(cipher_data) if type(cipher_data) is str else cipher_data
    except:
      raise ValueError("Incomplete or malformed ASN.1 input.")

  def __load_asn1_by_hex(self, asn1_hex):
    asn1_bytes = unhexlify(asn1_hex)
    pkcs5_contents = PKCS5Sequence.load(asn1_bytes)
    pbes2_sequence = pkcs5_contents['0'].native
    self.__validate_asn1(pbes2_sequence)
    self.iv = pbes2_sequence['1']['1']['1']
    self.salt = pbes2_sequence['1']['0']['1']['0']
    self.iterations = pbes2_sequence['1']['0']['1']['1']
    self.key_size = pbes2_sequence['1']['1']['0']
    self.cipher_data = hexlify(pkcs5_contents['1'].native)

  def __supported_algs(self):
    return (
      self.AES_128_CBC_OID,
      self.AES_192_CBC_OID,
      self.AES_256_CBC_OID,
    )

  def __key_size_bytes(self):
    switcher = {
      self.AES_128_CBC_OID: 16,
      self.AES_192_CBC_OID: 24,
      self.AES_256_CBC_OID: 32,
    }
    return switcher.get(self.key_size)

  def __validate_asn1(self, pbes2):
    key_size = pbes2['1']['1']['0']
    pkcs_identifier = pbes2['0']
    pbkdf2_identifier = pbes2['1']['0']['0']
    digest_alg = pbes2['1']['0']['1']['2']['0']
    supported_algs = self.__supported_algs()
    if pkcs_identifier != self.PKCS5_OID:
      raise ValueError('Exception decoding bytes: Bytes are not PKCS5.')
    if pbkdf2_identifier != self.PBKDF2_OID:
      raise ValueError('Exception decoding bytes: Bytes are not pkcs5PBKDF2.')
    if key_size not in supported_algs:
      raise ValueError('Encryption algorithm not supported.')
    if digest_alg != self.HMAC_SHA256_OID:
      raise ValueError('Digest algorithm not supported.')

class PKCS5Sequence(Sequence):
  _fields = [
    ('0', Sequence), # PBES2Sequence
    ('1', OctetString), # Cipher data
  ]

class PBES2Sequence(Sequence):
  _fields = [
    ('0', ObjectIdentifier), #PKCS5_OID
    ('1', Sequence), # PBKDF2Sequence
  ]

class PBKDF2Sequence(Sequence):
  _fields = [
    ('0', Sequence), # PKInfoSequence
    ('1', Sequence), # IVKeySizeSequence
  ]

class PKInfoSequence(Sequence):
  _fields = [
    ('0', ObjectIdentifier), # PBKDF2_OID
    ('1', Sequence), #  KDFInfoSequence
  ]

class KDFInfoSequence(Sequence):
  _fields = [
    ('0', OctetString), # Salt
    ('1', Integer), # Iterations
    ('2', Sequence), # AlgSequence
  ]

class AlgSequence(Sequence):
  _fields = [
    ('0', ObjectIdentifier), # HMAC_SHA256_OID
  ]

class IVKeySizeSequence(Sequence):
  _fields = [
    ('0', ObjectIdentifier), # Key Size (AES_128_CBC_OID)
    ('1', OctetString), # IV
  ]
