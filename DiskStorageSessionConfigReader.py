import os.path
import json


class DiskStorageSessionConfigReader:

    sessions_dir = 'sessions'
    json_ext = '.json'

    # expects session id and config id
    # returns the session config path
    @staticmethod
    def get_config_path(session_id, config_id):
        sessions_path = DiskStorageSessionConfigReader.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        return os.path.join(session_path, config_id+DiskStorageSessionConfigReader.json_ext)

    # expects a keyword, contained in the config, a session id and a config_id
    # returns the corresponding value from the config
    @staticmethod
    def read_value(key, session_id, config_id):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        with open(config_path, encoding='utf8') as json_file:
            conf = json.load(json_file)
            if key in conf:
                return conf[key][0]
            else:
                return ''

    # expects a list of keywords, contained in the config, a session id and a config_id
    # returns the corresponding values from the config
    @staticmethod
    def read_values(keys, session_id, config_id):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        with open(config_path, encoding='utf8') as json_file:
            conf = json.load(json_file)
            values = list()
            for key in keys:
                if key in conf:
                    values.append(conf[key][0])
                else:
                    values.append('')
            return values

    # expects a session id, a config id and a json object
    # sets the session's config
    @staticmethod
    def set_config(session_id, config_id, json_f):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        with open(config_path, 'w+', encoding='utf8') as json_file:
            json.dump(json_f, json_file, ensure_ascii=False)

    # expects a session id and a config id
    # returns the session's config as json
    @staticmethod
    def get_config(session_id, config_id):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        with open(config_path, encoding='utf8') as json_file:
            return json.load(json_file)
