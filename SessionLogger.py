from DiskStorageSessionLogger import DiskStorageSessionLogger
from ConfigReader import ConfigReader


class SessionLogger:

    database_type_key = 'database-type'
    session_id_key = 'session-id'
    conf_id_key = 'config-id'
    db_type_fs = 'filesystem'

    # expects string to log
    # logs string
    @staticmethod
    def log(text: str, log_type='info'):
        conf_keys = list()
        conf_keys.append(SessionLogger.database_type_key)
        conf_keys.append(SessionLogger.session_id_key)
        conf_keys.append(SessionLogger.conf_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        session_id = conf_values[1]
        conf_id = conf_values[2]
        if db_type == SessionLogger.db_type_fs:
            DiskStorageSessionLogger.log(text, session_id, conf_id, log_type)

    # expects session id
    # deletes the log file
    @staticmethod
    def clear():
        conf_keys = list()
        conf_keys.append(SessionLogger.database_type_key)
        conf_keys.append(SessionLogger.session_id_key)
        conf_values = ConfigReader.read_values(conf_keys)
        db_type = conf_values[0]
        session_id = conf_values[1]
        if db_type == SessionLogger.db_type_fs:
            DiskStorageSessionLogger.clear(session_id)
