import unittest
import datetime as date
import sys
sys.path.append('../lib')
from Authenticator import *
from Config import *
import os
from TestUtils import *

class TestAuthenticator(unittest.TestCase):
  def test_authentication(self):
    simplejson = """
{
  "usersdbname": "testusers.db"
}
"""
    if os.path.exists("testusers.db"): os.remove("testusers.db")

    InitConfigFile("authconfig.json", simplejson)
    config = SimpleConfig("authconfig.json")
    auth = SimpleAuthenticator(config)

    self.assertTrue(auth.Register("pepe", "pepa"))
    self.assertFalse(auth.Register("pepe", "popa"))
    self.assertTrue(auth.Authenticate("pepe", "pepa"))
    self.assertFalse(auth.Authenticate("david", "pepa"))

    auth2 = SimpleAuthenticator(config)
    self.assertTrue(auth2.Registered("pepe"))
    self.assertFalse(auth2.Registered("lluisa"))
    self.assertTrue(auth2.Authenticate("pepe", "pepa"))
    self.assertFalse(auth2.Authenticate("david", "pepa"))

    os.remove("authconfig.json")

if __name__ == '__main__':
    unittest.main()