import json

class SimpleConfig:
  def __init__(self, filename) -> None:
    with open(filename) as config_file:
      config_data = config_file.read()

    self.parsed_config = json.loads(config_data)

  def Get(self, key):
    return self.parsed_config[key]

