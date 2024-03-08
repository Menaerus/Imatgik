import Config
import os
import sqlite3
from flask import send_file

class SimpleStorage:
  def __init__(self, config) -> None:
    self.storageroot = config.Get("storageroot", "images")
    self.rootparent = config.Get("storagerootparent", "static")
    self.realstorageroot = os.path.join(self.rootparent, self.storageroot)
    if not os.path.exists(self.rootparent):
      os.mkdir(self.rootparent)
    if not os.path.exists(self.realstorageroot):
      os.mkdir(self.realstorageroot)
    

  def _UserStorageName(self, userid):
    return os.path.join(self.realstorageroot, userid)
  
  def _UserStorageTitlesDb(self, userstoragename):
    return os.path.join(userstoragename, "titles.db")
  
  def _GenerateStoragename(self, userid, filename):
    userstoragename = self._UserStorageName(userid)
    if not os.path.exists(userstoragename):
      os.mkdir(userstoragename)
      if not os.path.exists(userstoragename):
        raise Exception("Could not create storage folder "+ userstoragename)
      usertitlestorage = self._UserStorageTitlesDb(userstoragename)
      con = sqlite3.connect(usertitlestorage)
      cur = con.cursor()
      if cur.execute("select name from sqlite_master").fetchone() is None:
        cur.execute("create table titles(filename, title)")
        con.commit()
      con.close()
    
    return os.path.join(userstoragename, filename)

  # store the title for that filename
  def StoreTitle(self, userid, filename, title):
    userstoragename = self._UserStorageName(userid)
    userstoragetitlesdb = self._UserStorageTitlesDb(userstoragename)
    con = sqlite3.connect(userstoragetitlesdb)
    cur = con.cursor()
    res = cur.execute("select title from titles where filename='%s'" % filename)
    if res != None:
      r = res.fetchone()
      if r != None:
        cur.execute("update titles set title='%s' where filename='%s'" % (title, filename))
        con.commit()
        con.close()
        return
    cur.execute("insert into titles values ('%s', '%s')" % (filename, title))
    con.commit()
    con.close()

  def _RemoveTitle(self, userid, filename):
    userstoragename = self._UserStorageName(userid)
    userstoragetitlesdb = self._UserStorageTitlesDb(userstoragename)
    con = sqlite3.connect(userstoragetitlesdb)
    cur = con.cursor()
    cur.execute("delete from titles where filename='%s'" % filename)
    con.commit()
    con.close()

  # obtain title for that filename
  def GetTitle(self, userid, filename):
    userstoragename = self._UserStorageName(userid)
    userstoragetitlesdb = self._UserStorageTitlesDb(userstoragename)
    title = None
    con = sqlite3.connect(userstoragetitlesdb)
    cur = con.cursor()
    res = cur.execute("select title from titles where filename='%s'" % filename)
    if res != None:
      r = res.fetchone()
      if r != None:
        (title, ) = r
    con.close()
    return title

  # store file with title
  def Store(self, userid, file, title):
    try:
      originalfilename = file.filename
      (_, simplefilename) = os.path.split(file.filename)
      filename = self._GenerateStoragename(userid, simplefilename)
      file.save(filename)
      self.StoreTitle(userid, simplefilename, title)
      return (originalfilename, filename)
    except Exception as e:
      print(e)
      return (None, None)
  
  def Remove(self, userid, filename):
    fullname = os.path.join(self.realstorageroot, userid, filename)
    if os.path.exists(fullname):
      os.remove(fullname)
      (_, simplefilename) = os.path.split(filename)
      self._RemoveTitle(userid, simplefilename) 

    
  def GetFilenames(self, userid):
    userstoragename = os.path.join(self.realstorageroot, userid)
    if os.path.exists(userstoragename):
      list = os.listdir(userstoragename)
      list.remove("titles.db")
      return list
    return []
  
  def CompleteName(self, userid, filename):
    userstoragename = self.storageroot+'/'+userid
    return userstoragename+'/'+filename


  def Send_File(self, userid, filename):
    userstoragename = os.path.join(self.realstorageroot, userid)
    if os.path.exists(userstoragename):
      fullname = os.path.join(self.realstorageroot, userid, filename)
      if os.path.exists(fullname):
        return send_file(fullname)
    return None