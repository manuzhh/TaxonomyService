import os.path
import json
from DiskStorageMisc import DiskStorageMisc


class DiskStorageSessionConfigReader:

    sessions_dir = 'sessions'
    json_ext = '.json'
    best_performing = 'best_performing'
    best_performing_f_name = 'session_conf_top_performing'

    # expects session id and config id
    # returns the session config path
    @staticmethod
    def get_config_path(session_id, config_id, create_sub_dirs=0, root_path=None):
        if config_id == DiskStorageSessionConfigReader.best_performing:
            return DiskStorageSessionConfigReader.best_performing_f_name
        sessions_path = DiskStorageSessionConfigReader.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        config_id = DiskStorageMisc.get_identifier_path(config_id, create_sub_dirs=create_sub_dirs, root_path=root_path)
        return os.path.join(session_path, config_id + DiskStorageSessionConfigReader.json_ext)

    # expects a keyword, contained in the config, a session id and a config_id
    # returns the corresponding value from the config
    @staticmethod
    def read_value(key, session_id, config_id):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        if os.path.exists(config_path):
            with open(config_path, encoding='utf8') as json_file:
                conf = json.load(json_file)
                if key in conf:
                    return conf[key][0]
                else:
                    return ''
        else:
            return ''

    # expects a list of keywords, contained in the config, a session id and a config_id
    # returns the corresponding values from the config
    @staticmethod
    def read_values(keys, session_id, config_id):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        if os.path.exists(config_path):
            with open(config_path, encoding='utf8') as json_file:
                conf = json.load(json_file)
                values = list()
                for key in keys:
                    if key in conf:
                        values.append(conf[key][0])
                    else:
                        values.append('')
                return values
        else:
            return list()

    # expects a session id, a config id and a json object
    # sets the session's config
    @staticmethod
    def set_config(session_id, config_id, json_f):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id, create_sub_dirs=1, root_path=DiskStorageMisc.get_session_path(session_id))
        with open(config_path, 'w+', encoding='utf8') as json_file:
            json.dump(json_f, json_file, ensure_ascii=False, indent=4)

    # expects a session id and a config id
    # returns the session's config as json
    @staticmethod
    def get_config(session_id, config_id):
        config_path = DiskStorageSessionConfigReader.get_config_path(session_id, config_id)
        if os.path.exists(config_path):
            with open(config_path, encoding='utf8') as json_file:
                return json.load(json_file)
        else:
            return {}

    # expects a json object
    # sets the currently best performing config
    @staticmethod
    def set_best_performing(json_f):
        config_path = DiskStorageSessionConfigReader.best_performing_f_name
        with open(config_path, 'w+', encoding='utf8') as json_file:
            json.dump(json_f, json_file, ensure_ascii=False, indent=4)

    # expects a session id and a config id
    # sets the currently best performing config
    @staticmethod
    def set_best_performing_by_ids(session_id, config_id):
        conf = DiskStorageSessionConfigReader.get_config(session_id, config_id)
        DiskStorageSessionConfigReader.set_best_performing(conf)

    # returns the currently best performing config
    @staticmethod
    def get_best_performing():
        return DiskStorageSessionConfigReader.get_config('xyz', DiskStorageSessionConfigReader.best_performing)
