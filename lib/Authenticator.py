import hashlib
import sqlite3

class SimpleAuthenticator:
  def __init__(self, config) -> None:
    self.con = sqlite3.connect(config.Get("usersdbname", "users.db"))
    cur = self.con.cursor()
    if cur.execute("select name from sqlite_master").fetchone() is None:
      cur.execute("create table users(username, password)")
      cur.execute("insert into users values ('david', '778d5bd89816d7d0c78070bf27cf2d8b')")
      self.con.commit()

  def Authenticate(self, user, password):
    md5 = hashlib.md5((user+password).encode()).hexdigest()
    cur = self.con.cursor()
    res = cur.execute("select * from users where username = '%s' and password = '%s'" % (user, str(md5)))
    if res.fetchone() is None: return False
    return True
  
  def Registered(self, user):
    cur = self.con.cursor()
    res = cur.execute("select * from users where username = '%s'" % user)
    return res.fetchone( )!= None

  def Register(self, user, password):
    if self.Registered(user): return False
    md5 = hashlib.md5((user+password).encode()).hexdigest()
    cur = self.con.cursor()
    cur.execute("insert into users values ('%s','%s')" % (user, str(md5)))
    self.con.commit()
    return True

  
