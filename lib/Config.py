import json

class SimpleConfig:
  def __init__(self, filename) -> None:
    with open(filename) as config_file:
      config_data = config_file.read()

    self.parsed_config = json.loads(config_data)

  def Get(self, key, default=None):
    if key in self.parsed_config.keys():
      return self.parsed_config[key]
    else:
      if default == None:
        raise KeyError
      else:
        return default

