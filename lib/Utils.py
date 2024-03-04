import hashlib

def Scramble(username, password):
  return hashlib.md5((username+password).encode()).hexdigest()