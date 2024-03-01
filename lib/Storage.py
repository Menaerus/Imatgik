import Config
import os

class SimpleStorage:
  def __init__(self, config) -> None:
    self.storageroot = config.Get("storageroot", "images")
    if not os.path.exists(self.storageroot):
      os.mkdir(self.storageroot)
    
  def GenerateStoragename(self, username, filename):
    userstoragename = os.path.join(self.storageroot, username)
    if not os.path.exists(userstoragename):
      os.mkdir(userstoragename)
    
    return os.path.join(userstoragename, filename)


  def Store(self, username, file):
    originalfilename = file.filename
    (_, simplefilename) = os.path.split(file.filename)
    filename = self.GenerateStoragename(username, simplefilename)
    file.save(filename)
    return (originalfilename, filename)
  
  def Remove(self, filename):
    fullname = os.path.join(self.storageroot, filename)
    if os.path.exists(fullname): os.remove(fullname)

    
  def GetFilenames(self, username):
    userstoragename = os.path.join(self.storageroot, username)
    if os.path.exists(userstoragename): return os.listdir(userstoragename)
    return []
  
