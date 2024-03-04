from Utils import *

class User:
  # implementation of the wrapper needed by flask-login
  def __init__(self, username, password) -> None:
    self.username = username
    self.userid = Scramble(username, password)
    self.is_authenticated = False
    self.is_active = False
    self.is_anonymous = False
    self.images = []

  # 
  def ReCreate(self, userid) -> None:
    self.userid = userid
    self.is_authenticated = True
    self.is_active = True
    self.is_anonymous = False
    self.images = []

  def get_id(self):
    return self.userid
  
  def get(userid, authenticator, storage):
    (username, found) =  authenticator.RegisteredWithUserid(userid)
    if found:
      user = User(username, '')
      user.ReCreate(userid)
      user.Fill(storage)
      return user
    return None
  
  def Fill(self, storage):
    self.images = storage.GetFilenames(self.userid)
