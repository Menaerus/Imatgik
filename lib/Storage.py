import Config
import os

class SimpleStorage:
  def __init__(self, config) -> None:
    self.storageroot = config.Get("storageroot", "images")
    self.rootparent = config.Get("storagerootparent", "static")
    self.realstorageroot = os.path.join(self.rootparent, self.storageroot)
    if not os.path.exists(self.rootparent):
      os.mkdir(self.rootparent)
    if not os.path.exists(self.realstorageroot):
      os.mkdir(self.realstorageroot)
    
  def GenerateStoragename(self, userid, filename):
    userstoragename = os.path.join(self.realstorageroot, userid)
    if not os.path.exists(userstoragename):
      os.mkdir(userstoragename)
    
    return os.path.join(userstoragename, filename)


  def Store(self, userid, file):
    try:
      originalfilename = file.filename
      (_, simplefilename) = os.path.split(file.filename)
      filename = self.GenerateStoragename(userid, simplefilename)
      file.save(filename)
      return (originalfilename, filename)
    except Exception:
      return (None, None)
  
  def Remove(self, userid, filename):
    fullname = os.path.join(self.realstorageroot, os.path.join(userid, filename))
    if os.path.exists(fullname): os.remove(fullname)

    
  def GetFilenames(self, userid):
    userstoragename = os.path.join(self.realstorageroot, userid)
    if os.path.exists(userstoragename): return os.listdir(userstoragename)
    return []
  
  def CompleteName(self, userid, filename):
    userstoragename = self.storageroot+'/'+userid
    return userstoragename+'/'+filename

