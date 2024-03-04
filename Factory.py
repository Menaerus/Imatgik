import sys
sys.path.append('./lib')

from Storage import *
from Authenticator import *

def MakeStorage(config):
  return SimpleStorage(config)

def MakeAuthenticator(config):
  return SimpleAuthenticator(config)
