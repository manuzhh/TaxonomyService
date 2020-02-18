import os.path
import json


class DiskStorageSessionConfigReader:

    sessions_dir = 'sessions'
    json_ext = '.json'

    # expects a keyword, contained in the config, a session id and a config_id
    # returns the corresponding value from the config
    @staticmethod
    def read_value(key, session_id, config_id):
        sessions_path = DiskStorageSessionConfigReader.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        config_path = os.path.join(session_path, config_id+DiskStorageSessionConfigReader.json_ext)
        with open(config_path, encoding='utf8') as json_file:
            conf = json.load(json_file)
            return conf[key][0]

    # expects a list of keywords, contained in the config, a session id and a config_id
    # returns the corresponding values from the config
    @staticmethod
    def read_values(keys, session_id, config_id):
        sessions_path = DiskStorageSessionConfigReader.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        config_path = os.path.join(session_path, config_id+DiskStorageSessionConfigReader.json_ext)
        with open(config_path, encoding='utf8') as json_file:
            conf = json.load(json_file)
            values = list()
            for key in keys:
                values.append(conf[key][0])
            return values
