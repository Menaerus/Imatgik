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
    if os.path.exists("static/images"): rmtree("static/images")
    storage = SimpleStorage(simpleconfig)
    self.assertTrue(os.path.exists(os.path.join("static", "images")))

  def test_storagefoldernamegeneration(self):
     if os.path.exists("static/images/david"): rmtree("static/images/david")
     storage = SimpleStorage(simpleconfig)
     self.assertEqual(os.path.join(os.path.join(os.path.join("static", "images"), "david"), "Imatge.jpg"), storage._GenerateStoragename("david", "Imatge.jpg"))
     self.assertTrue(os.path.exists(os.path.join(os.path.join("static", "images"), "david")))


  def test_upload(self):
     if os.path.exists("static/images/david"): 
       rmtree("static/images/david")
     storage = SimpleStorage(simpleconfig)
     with open(os.path.join("testimages", "Imatge1.png"), 'rb') as fp:
       file = FileStorage(fp)
       (original, new) = storage.Store("david", file, "My image")

     self.assertTrue(os.path.exists(new))
     self.assertTrue(cmp(original, new))
     files = storage.GetFilenames("david")
     self.assertEqual(len(files), 1)
     self.assertEqual(files[0], "Imatge1.png")
     title = storage.GetTitle("david", "Imatge1.png")
     self.assertEqual(title, "My image") 
     files = storage.GetFilenames("pepe")
     self.assertEqual(len(files), 0)
    
     storage.Remove("david", new)

  def test_edittitle(self):
    if os.path.exists("static/images/david"): 
      rmtree("static/images/david")
    storage = SimpleStorage(simpleconfig)
    with open(os.path.join("testimages", "Imatge1.png"), 'rb') as fp:
      file = FileStorage(fp)
      (original, new) = storage.Store("david", file, "My image")

    title = storage.GetTitle("david", "Imatge1.png")
    self.assertEqual(title, "My image") 
    storage.StoreTitle("david", "Imatge1.png", "Really My image")
    self.assertEqual(storage.GetTitle("david", "Imatge1.png"), "Really My image")
    
  def test_remove(self):   
    if os.path.exists("static/images/david"): 
      rmtree("static/images/david")
    storage = SimpleStorage(simpleconfig)
    with open(os.path.join("testimages", "Imatge1.png"), 'rb') as fp:
      file = FileStorage(fp)
      (original, new) = storage.Store("david", file, "My image")

    files = storage.GetFilenames("david")
    self.assertEqual(len(files), 1)
    self.assertEqual(files[0], "Imatge1.png")
    title = storage.GetTitle("david", "Imatge1.png")
    self.assertEqual(title, "My image") 

    storage.Remove("david", "Imatge1.png")
    files = storage.GetFilenames("david")
    self.assertEqual(len(files), 0)
    title = storage.GetTitle("david", "Imatge1.png")
    self.assertEqual(title, None) 
    
if __name__ == '__main__':
    unittest.main()
