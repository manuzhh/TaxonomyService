import os.path
import os
import shutil
from SessionLogger import SessionLogger


class DiskStorageMisc:

    sessions_dir = 'sessions'
    data_dir = 'data'

    # expects session id
    # returns corresponding directory path for data
    @staticmethod
    def get_session_data_path(session_id):
        sessions_path = DiskStorageMisc.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        return os.path.join(session_path, DiskStorageMisc.data_dir)

    # expects session id
    # checks if the data folder is already created and creates it if not
    @staticmethod
    def create_data_folder(session_id):
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        if not os.path.exists(data_path):
            os.makedirs(data_path)

    # expects path to folder
    # deletes all files from folder
    @staticmethod
    def delete_from_folder(path):
        if os.path.exists(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    SessionLogger.log('Failed to delete %s. Reason: %s' % (file_path, e))

    # expects session identifier
    # deletes all data from session
    @staticmethod
    def delete_session_data(session_id):
        folder = DiskStorageMisc.get_session_data_path(session_id)
        DiskStorageMisc.delete_from_folder(folder)
        SessionLogger.log('All session data has been deleted.')
