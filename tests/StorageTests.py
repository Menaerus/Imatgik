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


def upload(userid, filename, title):
  if os.path.exists(os.path.join("static","images", userid)): 
      rmtree(os.path.join("static","images", userid))
  storage = SimpleStorage(simpleconfig)
  with open(os.path.join("testimages", filename), 'rb') as fp:
    file = FileStorage(fp)      
    (original, new) = storage.Store(userid, file, title)
  return (storage, original, new)


class TestStorage(unittest.TestCase):
  def test_ifstoragecreatestheimagesfolder(self):
    if os.path.exists(os.path.join("static", "images")): rmtree(os.path.join("static", "images"))
    storage = SimpleStorage(simpleconfig)
    self.assertTrue(os.path.exists(os.path.join("static", "images")))

  def test_storagefoldernamegeneration(self):
     if os.path.exists(os.path.join("static", "images", "david")): rmtree(os.path.join("static", "images", "david"))
     storage = SimpleStorage(simpleconfig)
     self.assertEqual(os.path.join("static", "images", "david", "Imatge.jpg"), storage._GenerateStoragename("david", "Imatge.jpg"))
     self.assertTrue(os.path.exists(os.path.join("static", "images", "david")))

  
  def do_test_upload(self, userid, filename, title):
    (storage, original, new) = upload(userid, filename, title)

    self.assertTrue(os.path.exists(new))
    self.assertTrue(cmp(original, new))
    files = storage.GetFilenames(userid)
    self.assertEqual(len(files), 1)
    self.assertEqual(files[0], filename)
    thetitle = storage.GetTitle(userid, filename)
    self.assertEqual(thetitle, title) 
    
  
    storage.Remove(userid, filename)
    self.assertFalse(os.path.exists(os.path.join("static", "images", userid, filename)))
    self.assertEqual(storage.GetTitle(userid, filename), None)

  def test_upload(self):
    self.do_test_upload("david", "Imatge1.png", "My title")
    self.do_test_upload("4a1450f72fc01ffc5ef38d337f71eef9", "Imatge1.png", "Her title")
    
  def test_nofolderforunknownuser(self):  
    storage = SimpleStorage(simpleconfig)
    files = storage.GetFilenames("pepe")
    self.assertEqual(len(files), 0)

  def test_edittitle(self):
    (storage, _, _) = upload("david", "Imatge1.png", "My image")

    title = storage.GetTitle("david", "Imatge1.png")
    self.assertEqual(title, "My image") 
    storage.StoreTitle("david", "Imatge1.png", "Really My image")
    self.assertEqual(storage.GetTitle("david", "Imatge1.png"), "Really My image")
    
  def test_remove(self):  
    (storage, _, _) = upload("david", "Imatge1.png", "My title") 

    files = storage.GetFilenames("david")
    self.assertEqual(len(files), 1)
    self.assertEqual(files[0], "Imatge1.png")
    title = storage.GetTitle("david", "Imatge1.png")
    self.assertEqual(title, "My title") 

    storage.Remove("david", "Imatge1.png")
    files = storage.GetFilenames("david")
    self.assertEqual(len(files), 0)
    title = storage.GetTitle("david", "Imatge1.png")
    self.assertEqual(title, None) 
    
if __name__ == '__main__':
    unittest.main()
