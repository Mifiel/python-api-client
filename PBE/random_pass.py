import binascii
from Crypto.Hash import SHA256, SHA, HMAC
from Crypto.Protocol.KDF import PBKDF2
import random, string, os

class RandomPass:
    MIN_ITERATIONS = 1000
    MAX_ITERATIONS = 99999
    MAX_KEY_LENGTH = 1000
    MIN_SALT_LENGTH = 16

    def get_derived_key(self, password, salt, num_iterations, size_key):
        if num_iterations < self.MIN_ITERATIONS:
            return 'number of iterations too short'
        if num_iterations > self.MAX_ITERATIONS:
            return 'number of iterations too long'
        if size_key > self.MAX_KEY_LENGTH:
            return 'key length too long'
        if len(salt) < self.MIN_SALT_LENGTH:
            return 'salt length is too short'

        key = PBKDF2(password, salt, dkLen=size_key, count =num_iterations, prf = lambda p,s: HMAC.new(p,s,SHA256).digest())
        return binascii.hexlify(key)

    def secure_random(self, length = 16):
        myrg = random.SystemRandom()
        alphabet = string.ascii_letters + string.digits + "-_+=#&*."
        pw = str().join(myrg.choice(alphabet) for _ in range(length))
        return pw

    def random_salt(self, salt_size = 16):
        return os.urandom(salt_size)
