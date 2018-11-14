import pytest
from random_pass import RandomPass

class TestRandomPass:
    @pytest.fixture
    def params(self):
        return { "valid": [ { "key": "passwd", "salt": "salt", "iterations": 1, "keylen": 64, "result": "55ac046e56e3089fec1691c22544b605f94185216dde0465e68b9d57c20dacbc49ca9cccf179b645991664b39d77ef317c71b845b1e30bd509112041d3a19783" }, { "key": "Password", "salt": "NaCl", "iterations": 80000, "keylen": 64, "result": "4ddcd8f60b98be21830cee5ef22701f9641a4418d04c0414aeff08876b34ab56a1d425a1225833549adb841b51c9b3176a272bdebba1d078478f62b397f33c8d" }, { "key": "password", "salt": "salt", "iterations": 1, "keylen": 32, "result": "120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b" }, { "key": "password", "salt": "salt", "iterations": 2, "keylen": 32, "result": "ae4d0c95af6b46d32d0adff928f06dd02a303f8ef3c251dfd6e2d85a95474c43" }, { "key": "password", "salt": "salt", "iterations": 4096, "keylen": 32, "result": "c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a" }, { "key": "passwordPASSWORDpassword", "salt": "saltSALTsaltSALTsaltSALTsaltSALTsalt", "iterations": 4096, "keylen": 40, "result": "348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c4e2a1fb8dd53e1c635518c7dac47e9" }, { "key": "", "salt": "salt", "iterations": 1024, "keylen": 32, "result": "9e83f279c040f2a11aa4a02b24c418f2d3cb39560c9627fa4f47e3bcc2897c3d" }, { "key": "password", "salt": "", "iterations": 1024, "keylen": 32, "result": "ea5808411eb0c7e830deab55096cee582761e22a9bc034e3ece925225b07bf46" } ], "invalid": [ { "key": "password", "salt": "afas", "iterations": 1024, "keylen": 35184372088832, "result": "", "description": "key length too long" } ] }

    def test_get_derived_key(self, params):
        for test in params['valid']:
            rp = RandomPass()
            result = rp.get_derived_key(test['key'], test['salt'], test['iterations'], test['keylen'])
            assert test['result'] == result
