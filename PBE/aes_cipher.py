import binascii
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def encrypt(self, key, document, iv):
        return '0'

    def decrypt(self, key, encrypted_document, iv):
        ed = binascii.unhexlify(encrypted_document)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        result = unpad(cipher.decrypt(ed), AES.block_size)
        return result

