import os.path
import logging
from datetime import datetime


class DiskStorageSessionLogger:

    sessions_dir = 'sessions'
    log_ext = '.log'

    # expects session id
    # returns path to log file
    @staticmethod
    def get_log_path(session_id: str):
        sessions_path = DiskStorageSessionLogger.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        return os.path.join(session_path, session_id+DiskStorageSessionLogger.log_ext)

    # expects string to log, a session id and a config id
    # logs string
    @staticmethod
    def log(text: str, session_id: str, conf_id: str, log_type='info'):
        log_path = DiskStorageSessionLogger.get_log_path(session_id)
        log_text = ' ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + session_id + ' (' + conf_id + ') > ' + text
        logging.basicConfig(filename=log_path, level=logging.DEBUG)
        if log_type == 'debug':
            logging.debug(log_text)
        elif log_type == 'warning':
            logging.warning(log_text)
        elif log_type == 'error':
            logging.error(log_text)
        else:
            logging.info(log_text)

    # expects session id
    # deletes the log file
    @staticmethod
    def clear(session_id: str):
        log_path = DiskStorageSessionLogger.get_log_path(session_id)
        open(log_path, 'w').close()
