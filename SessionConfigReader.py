import json
from DiskStorageSessionConfigReader import DiskStorageSessionConfigReader
from ConfigReader import ConfigReader


class SessionConfigReader:

    database_type_key = 'database-type'
    config_id_key = 'config-id'
    session_id_key = 'session-id'
    db_type_fs = 'filesystem'
    config_template_key = 'config-template-id'
    config_template_default = 'default'
    config_template_default_name = 'session_config_template.json'

    # returns session id
    @staticmethod
    def get_session_id():
        return ConfigReader.read_value(SessionConfigReader.session_id_key)

    # returns config id
    @staticmethod
    def get_config_id():
        return ConfigReader.read_value(SessionConfigReader.config_id_key)

    # expects a keyword, contained in the config
    # returns the corresponding value from the config
    @staticmethod
    def read_value(key):
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_id_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        config_id = conf_values[1]
        session_id = conf_values[2]
        if db_type == SessionConfigReader.db_type_fs:
            return DiskStorageSessionConfigReader.read_value(key, session_id, config_id)
        else:
            return ''

    # expects a list of keywords, contained in the config
    # returns the corresponding values from the config
    @staticmethod
    def read_values(keys):
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_id_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        config_id = conf_values[1]
        session_id = conf_values[2]
        if db_type == SessionConfigReader.db_type_fs:
            return DiskStorageSessionConfigReader.read_values(keys, session_id, config_id)
        else:
            return list()

    # expects a json object
    # sets the session's config
    @staticmethod
    def set_config(json_f, config_id=None):
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_id_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        if config_id is None:
            config_id = conf_values[1]
        session_id = conf_values[2]
        if db_type == SessionConfigReader.db_type_fs:
            DiskStorageSessionConfigReader.set_config(session_id, config_id, json_f)

    # returns the session's config as json
    @staticmethod
    def get_config():
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_id_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        config_id = conf_values[1]
        session_id = conf_values[2]
        if db_type == SessionConfigReader.db_type_fs:
            return DiskStorageSessionConfigReader.get_config(session_id, config_id)
        else:
            return {}

    # returns the session config template as json
    @staticmethod
    def get_config_template(config_template_id=None):
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_template_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        if config_template_id is None:
            config_template_id = conf_values[1]
        session_id = conf_values[2]
        if config_template_id == SessionConfigReader.config_template_default:
            with open(SessionConfigReader.config_template_default_name, encoding='utf8') as json_file:
                return json.load(json_file)
        if db_type == SessionConfigReader.db_type_fs:
            return DiskStorageSessionConfigReader.get_config(session_id, config_template_id)
        else:
            return {}

    # expects a json object
    # sets the currently best performing config
    @staticmethod
    def set_best_performing(json_f):
        db_type = ConfigReader.get_db_type()
        if db_type == SessionConfigReader.db_type_fs:
            DiskStorageSessionConfigReader.set_best_performing(json_f)

    # expects a session id and a config id
    # sets the currently best performing config
    @staticmethod
    def set_best_performing_by_ids(session_id=None, config_id=None):
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_id_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        if config_id is None:
            config_id = conf_values[1]
        if session_id is None:
            session_id = conf_values[2]
        if db_type == SessionConfigReader.db_type_fs:
            DiskStorageSessionConfigReader.set_best_performing_by_ids(session_id, config_id)

    # returns the currently best performing config
    @staticmethod
    def get_best_performing():
        db_type = ConfigReader.get_db_type()
        if db_type == SessionConfigReader.db_type_fs:
            return DiskStorageSessionConfigReader.get_best_performing()
