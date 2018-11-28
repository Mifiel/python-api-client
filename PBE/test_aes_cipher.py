import pytest, re
from aes_cipher import AESCipher

class TestAESCipher:
    @pytest.fixture
    def params(self):
        return [
            {
                "algotithm": "AES-128",
                "key": "1234567890123456",
                "dataToEncrypt": "cifrado de Prueba",
                "iv": "6976207465737469",
                "encrypted": "e69522e578832e378221b541431e64e6e704c17d8b2bdda598ebd3c716836d03"
            },
            {
                "algotithm": "AES-128",
                "key": "derivedKEY234556",
                "dataToEncrypt": "test de cifrado",
                "iv": "3436353837383837",
                "encrypted": "2b27f69570049490f5fee3bed8c045d9"
            },
            {
              "algotithm": "AES-128",
              "key": "a9r82*9rn5Flp3/o",
              "dataToEncrypt": "test de cifrado",
              "iv": "1353837383861646",
              "encrypted": "1b6a81b3ce5eb6ae3a239d0ee51e2699"
            },
            {
              "algotithm":"AES-192",
              "key": "123456789012345678901234",
              "dataToEncrypt": "cifrado de Prueba AES-192",
              "iv": "6466736438373435",
              "encrypted": "0cf4ea5765b42b9088c901064c07ba7a6eec3030609673830fcbd8ac5cc77edd"
            },
            {
              "algotithm":"AES-192",
              "key": "derivedKEY234556iksRtryr",
              "dataToEncrypt": "test de cifrado AES-192",
              "iv": "7266736438373435",
              "encrypted": "fd0fec1268dbb111babc5b8a15397ad946af61561eb6d40c36068c04ddf5d008"
            },
            {
              "algotithm":"AES-192",
              "key": "*854FrGTH/hgf_4f6h9v4dfg",
              "dataToEncrypt": "encrypted decrypted data",
              "iv": "2e39746438373435",
              "encrypted": "43e7e6f7a56a73a60d5b619e590b91de3c79e765a37f893f122a6b3e9497f8f6"
            },
            {
              "algotithm":"AES-256",
              "key": "12345678901234567890123456789012",
              "dataToEncrypt": "cifrado de Prueba AES-256",
              "iv": "39382e2e2d6438rf",
              "encrypted": "60ea45d407514d4e67ef0eb12b2df8e5ea02f156cdea71eeafda0b0b54092d63"
            },
            {
              "algotithm":"AES-256",
              "key": "derivedKEY234556iksRtryrtg578hfr",
              "dataToEncrypt": "test de cifrado AES-256",
              "iv": "7266736438373435",
              "encrypted": "6d2e185278b5a87da86941b390ac7baffee5e87ae86d877350edbe9a6077e396"
            },
            {
              "algotithm":"AES-256",
              "key": "*854FrGTH/hgf_4f6h9v4dfg*&jr-jew",
              "dataToEncrypt": "test de cifrado",
              "iv": "2e39746438373435",
              "encrypted": "3c3dc5a978f756a576a952b4eb3ca868"
            },
        ]

    def test_ecrypt(self, params):
        for test in params:
            cipher = AESCipher()
            result = cipher.encrypt(test["key"], test["dataToEncrypt"], test["iv"])
            assert test["encrypted"] == result

    def test_decrypt(self, params):
        for test in params:
            cipher = AESCipher()
            result = cipher.decrypt(test["key"], test["encrypted"], test["iv"])
            assert test["dataToEncrypt"] == result

    def test_iv(self, params):
        assert len(AESCipher().iv()) == 16
        assert re.match('[a-zA-Z0-9-_+=#&*.]', AESCipher().iv())

