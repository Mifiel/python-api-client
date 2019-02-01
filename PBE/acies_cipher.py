from ecies import encrypt, decrypt

class ECIESCipher:
    def encrypt(self, publicKey, message):
        encrypt(publicKey, str.encode(message))

    def decrypt(self, privateKey, encryptedStructure):
        decrypt(privateKey, encryptedStructure)

#  {
#    publicKey: 0246d04f5ee3a82a64822141e2c9177774d3fb1754e29af158a941005b6e453ef2
#    privateKey: 3fdbe675ffe10b5d646b3e20a16ec4f44c90374a42d00236f9e2b51ab6cdee16
#    encryptedData: {
#      iv: 9b225e38a7b8534a31c5792f504a13a7
#      ephemPublicKey: 047cd7ea12facf505add8b319f6da43fa59294eec219ebc99abbc7ac42f32142916f070476f91bc4c8431bebb3d43288f739fc8554fc778291137e918425497b83
#      ciphertext: 7547a6868c2e476e9e16351590542b48be9e297a32f63bfd519fb10714ede573
#      mac: 06a2108eb960ced35dedd149fd9bad4cb987809341a99544c8311749fbfc60c6
#    }
#    decrypted: 'Mensaje cifrado con ECIES!!! '
#    publicKey uncompress: 0446d04f5ee3a82a64822141e2c9177774d3fb1754e29af158a941005b6e453ef29b36cc0e63003c38a752bb159868919e0f3deef4ad56cdf84490ac3022034fd6
#  }

#  import collections
#  import hashlib
#  import random
#  import binascii
#  import sys
#  from hashlib import md5
#  from base64 import b64decode
#  from base64 import b64encode
#  from Crypto.Cipher import AES

#  def enc_long(n):
    #  '''Encodes arbitrarily large number n to a sequence of bytes.
    #  Big endian byte order is used.'''
    #  s = ""
    #  while n > 0:
        #  s = chr(n & 0xFF) + s
        #  n >>= 8
    #  return s

#  # Padding for the input string --not
#  # related to encryption itself.
#  BLOCK_SIZE = 16  # Bytes
#  pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                #  chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
#  unpad = lambda s: s[:-ord(s[len(s) - 1:])]


#  class AESCipher:
    #  """
    #  Usage:
        #  c = AESCipher('password').encrypt('message')
        #  m = AESCipher('password').decrypt(c)
    #  Tested under Python 3 and PyCrypto 2.6.1.
    #  """

    #  def __init__(self, key):
        #  self.key = key

    #  def encrypt(self, raw):
        #  raw = pad(raw)
        #  cipher = AES.new(self.key, AES.MODE_ECB)
        #  return b64encode(cipher.encrypt(raw))

    #  def decrypt(self, enc):
        #  enc = b64decode(enc)
        #  cipher = AES.new(self.key, AES.MODE_ECB)
        #  return unpad(cipher.decrypt(enc)).decode('utf8')


#  EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

#  curve = EllipticCurve(
    #  'secp256k1',
    #  # Field characteristic.
    #  p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    #  # Curve coefficients.
    #  a=0,
    #  b=7,
    #  # Base point.
    #  g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       #  0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    #  # Subgroup order.
    #  n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    #  # Subgroup cofactor.
    #  h=1,
#  )


#  # Modular arithmetic ##########################################################

#  def inverse_mod(k, p):
    #  """Returns the inverse of k modulo p.
    #  This function returns the only integer x such that (x * k) % p == 1.
    #  k must be non-zero and p must be a prime.
    #  """
    #  if k == 0:
        #  raise ZeroDivisionError('division by zero')

    #  if k < 0:
        #  # k ** -1 = p - (-k) ** -1  (mod p)
        #  return p - inverse_mod(-k, p)

    #  # Extended Euclidean algorithm.
    #  s, old_s = 0, 1
    #  t, old_t = 1, 0
    #  r, old_r = p, k

    #  while r != 0:
        #  quotient = old_r // r
        #  old_r, r = r, old_r - quotient * r
        #  old_s, s = s, old_s - quotient * s
        #  old_t, t = t, old_t - quotient * t

    #  gcd, x, y = old_r, old_s, old_t

    #  assert gcd == 1
    #  assert (k * x) % p == 1

    #  return x % p


#  # Functions that work on curve points #########################################

#  def is_on_curve(point):
    #  """Returns True if the given point lies on the elliptic curve."""
    #  if point is None:
        #  # None represents the point at infinity.
        #  return True

    #  x, y = point

    #  return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


#  def point_neg(point):
    #  """Returns -point."""
    #  assert is_on_curve(point)

    #  if point is None:
        #  # -0 = 0
        #  return None

    #  x, y = point
    #  result = (x, -y % curve.p)

    #  assert is_on_curve(result)

    #  return result


#  def point_add(point1, point2):
    #  """Returns the result of point1 + point2 according to the group law."""
    #  assert is_on_curve(point1)
    #  assert is_on_curve(point2)

    #  if point1 is None:
        #  # 0 + point2 = point2
        #  return point2
    #  if point2 is None:
        #  # point1 + 0 = point1
        #  return point1

    #  x1, y1 = point1
    #  x2, y2 = point2

    #  if x1 == x2 and y1 != y2:
        #  # point1 + (-point1) = 0
        #  return None

    #  if x1 == x2:
        #  # This is the case point1 == point2.
        #  m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    #  else:
        #  # This is the case point1 != point2.
        #  m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    #  x3 = m * m - x1 - x2
    #  y3 = y1 + m * (x3 - x1)
    #  result = (x3 % curve.p,
              #  -y3 % curve.p)

    #  assert is_on_curve(result)

    #  return result


#  def scalar_mult(k, point):
    #  """Returns k * point computed using the double and point_add algorithm."""
    #  assert is_on_curve(point)

    #  if k % curve.n == 0 or point is None:
        #  return None

    #  if k < 0:
        #  # k * point = -k * (-point)
        #  return scalar_mult(-k, point_neg(point))

    #  result = None
    #  addend = point

    #  while k:
        #  if k & 1:
            #  # Add.
            #  result = point_add(result, addend)

        #  # Double.
        #  addend = point_add(addend, addend)

        #  k >>= 1

    #  assert is_on_curve(result)

    #  return result


#  # Keypair generation and ECDSA ################################################

#  def make_keypair():
    #  """Generates a random private-public key pair."""
    #  private_key = random.randrange(1, curve.n)
    #  public_key = scalar_mult(private_key, curve.g)

    #  return private_key, public_key


#  def verify_signature(public_key, message, signature):
    #  z = hash_message(message)

    #  r, s = signature

    #  w = inverse_mod(s, curve.n)
    #  u1 = (z * w) % curve.n
    #  u2 = (r * w) % curve.n

    #  x, y = point_add(scalar_mult(u1, curve.g),
                     #  scalar_mult(u2, public_key))

    #  if (r % curve.n) == (x % curve.n):
        #  return 'signature matches'
    #  else:
        #  return 'invalid signature'


#  message="Hello"
#  if (len(sys.argv)>1):
        #  message=str(sys.argv[1])


#  private, public = make_keypair()
#  print "Private key:", hex(private)
#  print("Public key: (0x{:x}, 0x{:x})".format(*public))


#  print "========================="

#  r = 123456

#  print public

#  R = scalar_mult(r,curve.g)
#  S = scalar_mult(r,public)

#  print "======Symmetric key========"

#  print "Encryption key:",S[0]

#  cipher=AESCipher(enc_long(S[0])).encrypt(message)
#  print "Encrypted:\t",binascii.hexlify(cipher)

#  text=AESCipher(enc_long(S[0])).decrypt(cipher)

#  print "Decrypted:\t",text

