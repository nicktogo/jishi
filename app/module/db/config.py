import json
import os


class DbConfig:
    def __init__(self):
        module_dir = os.path.dirname(__file__)
        config_file_path = os.path.join(module_dir,'config.json')
        self.config_json_data = open(config_file_path)
        self.config_dict_data = json.loads(self.config_json_data.read())

    def get_config(self, db_name):
        return self.config_dict_data[db_name]

