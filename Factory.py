import sys
sys.path.append('./lib')

from Storage import *
from Authenticator import *

def MakeStorage(config):
  if config.Get("storagetype", "SimpleStorage") == "SimpleStorage":
    return SimpleStorage(config)
  return None

def MakeAuthenticator(config):
  if config.Get("authenticatortype", "SimpleAuthenticator"):
    return SimpleAuthenticator(config)
  return None
