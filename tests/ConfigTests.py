import unittest
import datetime as date
import sys
sys.path.append('../lib')
from Config import *
import os


class TestConfig(unittest.TestCase):
  def test_simple_gets(self):
    tests = [
      (
        """
        {
             "key1": "value1", 
             "key2": "value2"
        }
        """,
        [
          ('key1', 'value1'), ('key2', 'value2'), ('key3', None)
        ]
      ),
      (
        """
        {
             "key1": "", 
             "key2": "value2",
             "key2": "value22"
        }
        """,
        [
          ('key1', ''), ('key2', 'value22')
        ]
      )
    ]

    if os.path.exists("configunittests.json"): os.remove("configunittests.json")

    for (j, c) in tests:
      f = open("configunittests.json", "w+")
      f.write(j)
      f.close()
      config = SimpleConfig("configunittests.json")
      for (k, v) in c:
        try:
          self.assertEqual(v, config.Get(k))
        except KeyError:
          if v != None: self.fail()

    os.remove("configunittests.json")


  def test_gets_with_defaults(self):
      tests = [
        (
          """
          {
              "key1": "value1", 
              "key2": "value2"
          }
          """,
          [
            ('key1', 'value1', None), ('key2', 'value2', 'value3'), ('key3', 'value3', 'value3')
          ]
        ),
        (
          """
          {
              "key1": "", 
              "key2": "value2",
              "key2": "value22"
          }
          """,
          [
            ('key1', '', None), ('key2', 'value22', 'value2'), ('key3', None, None)
          ]
        )
      ]

      if os.path.exists("configunittests.json"): os.remove("configunittests.json")

      for (j, c) in tests:
        f = open("configunittests.json", "w+")
        f.write(j)
        f.close()
        config = SimpleConfig("configunittests.json")
        for (k, v, d) in c:
          try:
            self.assertEqual(v, config.Get(k, d))
          except KeyError:
            if v != None: self.fail()

      os.remove("configunittests.json")

if __name__ == '__main__':
    unittest.main()