import Config
import os

class SimpleStorage:
  def __init__(self, config) -> None:
    self.storageroot = config.Get("storageroot")

  def Store(self, username, file):
    originalfilename = file.filename
    filename = GenerateStoragename(self, username, file.filename)
    file.save(filename)
    return (originalfilename, filename)
  
  def Remove(self, filename):
    os.remove(ospath.join(self.storageroot, filename))

  def GenerateStoragename(self, username, filename):
    userstoragename = os.path.join(self.storageroot, username)
    if not os.path.exists(userstoragename):
      os.mkdir(userstoragename)
    
    return os.path.join(userstoragename, filename)
    
  def GetFilenames(self, username):
    userstoragename = os.path.join(self.storageroot, username)
    return os.listdir(userstoragename)
  
