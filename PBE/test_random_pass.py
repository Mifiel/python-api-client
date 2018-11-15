import pytest, re
from random_pass import RandomPass

class TestRandomPass:
    @pytest.fixture
    def params(self):
        return {
            "valid": [
                { "key": "passwordPASSWORDpassword", "salt": "saltSALTsaltSALTsaltSALTsaltSALTsalt", "iterations": 4096, "keylen": 40, "result": "348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c4e2a1fb8dd53e1c635518c7dac47e9" },
                { "key": "Password", "salt": "SALTsaltSALTsaltSALTsalt", "iterations": 1000, "keylen": 32, "result": "020321abe85e1644ac06c7db80c10398419ffb2e61bd5ce6c08f3d3fe48e7516" },
                { "key": "", "salt": "SALTsaltSALTsaltSALTsalt", "iterations": 1024, "keylen": 32, "result": "e935c382e26375594280a06013a7daba8df20c7ec10ad83b9bc4fd7d9f136c04" },
                { "key": "Password", "salt": "SALTsaltSALTsaltSALTsalt", "iterations": 80000, "keylen": 64, "result": "ecdbfbd5c912cf2933aa9d2bd2d5e9c3e48820c3f121ef9bc9c667b74a407f666b3ab32b0a8e74ce671b9515cb1b9ce9b785b87c87125f5c8bfdb6d3c4dae449" },
            ],
            "invalid": [
                { "key": "password", "salt": "afas", "iterations": 1024, "keylen": 35184372088832, "result": "", "description": "key length too long" },
                { "key": "password", "salt": "afas", "iterations": 1, "keylen": 64, "result": "", "description": "number of iterations too short" },
                { "key": "password", "salt": "afas", "iterations": 35184372088832, "keylen": 100, "result": "", "description": "number of iterations too long" },
                { "key": "password", "salt": "afas", "iterations": 1000, "keylen": 100, "result": "", "description": "salt length is too short" }
            ]
        }

    def test_valid_get_derived_key(self, params):
        for test in params['valid']:
            rp = RandomPass()
            result = rp.get_derived_key(test['key'], test['salt'], test['iterations'], test['keylen'])
            assert test['result'] == result

    def test_invalid_get_derived_key(self, params):
        for test in params['invalid']:
            rp = RandomPass()
            result = rp.get_derived_key(test['key'], test['salt'], test['iterations'], test['keylen'])
            assert test['description'] == result

    def test_random_salt(self, salt_size = 16):
        assert len(RandomPass().random_salt()) == 16
        assert len(RandomPass().random_salt(30)) == 30

    def test_secure_random(self, length = 16):
        assert len(RandomPass().secure_random()) == 16
        assert len(RandomPass().secure_random(32)) == 32
        assert re.match('[a-zA-Z0-9-_+=#&*.]', RandomPass().secure_random())
