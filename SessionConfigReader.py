from DiskStorageSessionConfigReader import DiskStorageSessionConfigReader
from ConfigReader import ConfigReader


class SessionConfigReader:

    database_type_key = 'database-type'
    config_id_key = 'config-id'
    session_id_key = 'session-id'
    db_type_fs = 'filesystem'

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
    def set_config(json_f):
        conf_keys = list()
        conf_keys.append(SessionConfigReader.database_type_key)
        conf_keys.append(SessionConfigReader.config_id_key)
        conf_keys.append(SessionConfigReader.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
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
