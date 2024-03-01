from werkzeug.datastructures import FileStorage
import unittest
import datetime as date
import sys
sys.path.append('../lib')
from Storage import *
from Config import *
import os
from TestUtils import *
from shutil import rmtree
from filecmp import cmp

simplejson = """
{
  "usersdbname": "testusers.db"
}
"""
InitConfigFile("testconfig.json", simplejson)
simpleconfig = SimpleConfig("testconfig.json")

class TestStorage(unittest.TestCase):
  def test_ifstoragecreatestheimagesfolder(self):
    if os.path.exists("images"): rmtree("images")
    storage = SimpleStorage(simpleconfig)
    self.assertTrue(os.path.exists("images"))

  def test_storagefoldernamegeneration(self):
     if os.path.exists("images/david"): rmtree("images/david")
     storage = SimpleStorage(simpleconfig)
     self.assertEqual(os.path.join(os.path.join("images", "david"), "imatge.jpg"), storage.GenerateStoragename("david", "imatge.jpg"))
     self.assertTrue(os.path.exists(os.path.join("images", "david")))


  def test_upload(self):
     if os.path.exists("images/david"): rmtree("images/david")
     storage = SimpleStorage(simpleconfig)
     with open(os.path.join("testimages", "imatge1.png"), 'rb') as fp:
       file = FileStorage(fp)
       (original, new) = storage.Store("david", file)

     self.assertTrue(os.path.exists(new))
     self.assertTrue(cmp(original, new))
     files = storage.GetFilenames("david")
     self.assertEqual(len(files), 1)
     self.assertEqual(files[0], "imatge1.png")
     files = storage.GetFilenames("pepe")
     self.assertEqual(len(files), 0)

     storage.Remove(new)

if __name__ == '__main__':
    unittest.main()
