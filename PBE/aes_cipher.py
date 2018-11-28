import binascii
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
import random, string

class AESCipher:
    def encrypt(self, key, dataToEncrypt, iv):
        key = str.encode(key)
        mode = AES.MODE_CBC
        iv = str.encode(iv)
        block_size = 16
        padded_text = pad(dataToEncrypt, block_size, style='pkcs7')
        e = AES.new(key, mode, iv)
        cipher_text = e.encrypt(padded_text)
        return binascii.hexlify(cipher_text)

    def decrypt(self, key, encrypted_document, iv):
        ed = binascii.unhexlify(encrypted_document)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        result = unpad(cipher.decrypt(ed), AES.block_size)
        return result

    def iv(self, length = 16):
        myrg = random.SystemRandom()
        alphabet = string.ascii_letters + string.digits + "-_+=#&*."
        result = str().join(myrg.choice(alphabet) for _ in range(length))
        return result

