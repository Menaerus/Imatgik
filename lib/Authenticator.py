import sqlite3
from Utils import *

class SimpleAuthenticator:
  def __init__(self, config) -> None:
    self.con = sqlite3.connect(config.Get("usersdbname", "users.db"))
    cur = self.con.cursor()
    if cur.execute("select name from sqlite_master").fetchone() is None:
      cur.execute("create table users(username, password)")
      self.con.commit()

  def Authenticate(self, user, password):
    md5 = Scramble(user, password)
    cur = self.con.cursor()
    res = cur.execute("select * from users where username = '%s' and password = '%s'" % (user, md5))
    if res.fetchone() is None: return False
    return True
  
  def Registered(self, user):
    cur = self.con.cursor()
    res = cur.execute("select * from users where username = '%s'" % user)
    return res.fetchone( )!= None

  def Register(self, user, password):
    if self.Registered(user): return False
    md5 = Scramble(user, password)
    cur = self.con.cursor()
    cur.execute("insert into users values ('%s','%s')" % (user, md5))
    self.con.commit()
    return True
  
  def RegisteredWithUserid(self, userid):
    cur = self.con.cursor()
    res = cur.execute("select username from users where password = '%s'" % userid)
    username = None
    if res != None: 
      r = res.fetchone()
      if r != None: (username,) = r
    return (username, username != None)
  
