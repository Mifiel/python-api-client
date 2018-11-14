import binascii
from Crypto.Hash import SHA256, SHA, HMAC
from Crypto.Protocol.KDF import PBKDF2
import random, string

class RandomPass:
    def get_derived_key(self, password, salt, num_iterations, size_key):
        key = PBKDF2(password, salt, dkLen=size_key, count =num_iterations, prf = lambda p,s: HMAC.new(p,s,SHA256).digest() )
        print(binascii.hexlify(key))
        return binascii.hexlify(key)

    def secure_random(self, length):
        myrg = random.SystemRandom()
        alphabet = string.ascii_letters + string.digits + "-_+=#&*."
        pw = str().join(myrg.choice(alphabet) for _ in range(length))
        return pw
