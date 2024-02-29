import hashlib

class SimpleAuthenticator:
  def __init__(self, config) -> None:
    self.users = { "david" : "778d5bd89816d7d0c78070bf27cf2d8b"}

  def Authenticate(self, user, password):
    md5 = hashlib.md5(user+password)
    if self.users[user] != None and self.users[user] == md5: return True
    return False
    
  
