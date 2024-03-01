import unittest
import datetime as date
import sys
sys.path.append('../lib')
from Storage import *
from Config import *
import os
from TestUtils import *

simplejson = """
{
  "usersdbname": "testusers.db"
}
"""
InitConfigFile("testconfig.json", simplejson)
simpleconfig = SimpleConfig("testconfig.json")

class TestStorage(unittest.TestCase):
  def test_ifstoragecreatestheimagesfolder(self):
    if os.path.exists("images/david"): os.rmdir("images/david")
    if os.path.exists("images"): os.rmdir("images")
    storage = SimpleStorage(simpleconfig)
    self.assertTrue(os.path.exists("images"))

  def test_storagefoldernamegeneration(self):
     if os.path.exists("images/david"): os.rmdir("images/david")
     storage = SimpleStorage(simpleconfig)
     self.assertEqual(os.path.join(os.path.join("images", "david"), "imatge.jpg"), storage.GenerateStoragename("david", "imatge.jpg"))
     self.assertTrue(os.path.exists("images/david"))

if __name__ == '__main__':
    unittest.main()
