import os.path
import json


class ConfigReader:

    config_name = 'config.json'
    database_type_key = 'database-type'
    config_id_key = 'config-id'
    session_id_key = 'session-id'

    # expects a keyword, contained in the config
    # returns the corresponding value from the config
    @staticmethod
    def read_value(key):
        #config_path = os.path.join('..', ConfigReader.config_name)
        config_path = ConfigReader.config_name
        with open(config_path) as json_file:
            conf = json.load(json_file)
            return conf[key]

    # expects a list of keywords, contained in the config
    # returns the corresponding values from the config
    @staticmethod
    def read_values(keys):
        #config_path = os.path.join('..', ConfigReader.config_name)
        config_path = ConfigReader.config_name
        with open(config_path) as json_file:
            conf = json.load(json_file)
            values = list()
            for key in keys:
                values.append(conf[key])
            return values

    # returns database type
    @staticmethod
    def get_db_type():
        return ConfigReader.read_value(ConfigReader.database_type_key)

    # returns session id
    @staticmethod
    def get_session_id():
        return ConfigReader.read_value(ConfigReader.session_id_key)

    # returns config id
    @staticmethod
    def get_config_id():
        return ConfigReader.read_value(ConfigReader.config_id_key)
