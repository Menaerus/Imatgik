import os

def InitConfigFile(filename, content):
  if os.path.exists(filename): os.remove(filename)

  f = open(filename, "w+")
  f.write(content)
  f.close()
