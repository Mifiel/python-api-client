from testlib import BaseTestCase
from mifiel.crypto import PBE

class TestPBE(BaseTestCase):
  FIXTURES = [
		{
			"key": "Password",
			"salt": "NaCl",
			"iterations": 80000,
			"keylen": 64,
			"result": "4ddcd8f60b98be21830cee5ef22701f9641a4418d04c0414aeff08876b34ab56a1d425a1225833549adb841b51c9b3176a272bdebba1d078478f62b397f33c8d"
		},
		{
			"key": "password",
			"salt": "salt",
			"iterations": 4096,
			"keylen": 32,
			"result": "c5e478d59288c841aa530db6845c4c8d962893a001ce4e11a4963873aa98134a",
		},
		{
			"key": "passwordPASSWORDpassword",
			"salt": "saltSALTsaltSALTsaltSALTsaltSALTsalt",
			"iterations": 4096,
			"keylen": 40,
			"result": "348c89dbcbd32b2f32d814b8116e84cf2b17347ebc1800181c4e2a1fb8dd53e1c635518c7dac47e9",
		},
		{
			"key": "",
			"salt": "salt",
			"iterations": 1024,
			"keylen": 32,
			"result": "9e83f279c040f2a11aa4a02b24c418f2d3cb39560c9627fa4f47e3bcc2897c3d",

		},
		{
			"key": "password",
			"salt": "",
			"iterations": 1024,
			"keylen": 32,
			"result": "ea5808411eb0c7e830deab55096cee582761e22a9bc034e3ece925225b07bf46",
		}
	]

  def test_random_password(self):
    passwordA = PBE.random_password(32)
    passwordB = PBE.random_password(48)
    passwordC = PBE.random_password(120)
    assert len(passwordA) == 32
    assert len(passwordB) == 48
    assert len(passwordC) == 120

  def test_random_salt(self):
    saltA = PBE.random_salt()
    saltB = PBE.random_salt(32)
    saltC = PBE.random_salt(64)
    assert len(saltA) == 16
    assert len(saltB) == 32
    assert len(saltC) == 64

  def test_random_salt_exception(self):
    with self.assertRaises(ValueError):
      PBE.random_salt(8)

  def test_get_derived_key(self):
    for test in self.FIXTURES:
      derived_key = PBE.get_derived_key(test['key'], size=test['keylen'], salt=test['salt'], iterations=test['iterations'])
      assert derived_key == test['result']

  def test_get_derived_key_exceptions(self):
    # Too much key len
    with self.assertRaises(ValueError):
      PBE.get_derived_key('password', size=1100)

    # Too much iterations
    with self.assertRaises(ValueError):
      PBE.get_derived_key('password', iterations=120000)

    # Few iterations
    with self.assertRaises(ValueError):
      PBE.get_derived_key('password', iterations=10)
