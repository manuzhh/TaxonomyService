import os.path
import os
import shutil
from SessionLogger import SessionLogger


class DiskStorageMisc:

    sessions_dir = 'sessions'
    data_dir = 'data'

    # expects session id
    # returns corresponding directory path for session
    @staticmethod
    def get_session_path(session_id):
        sessions_path = DiskStorageMisc.sessions_dir
        return os.path.join(sessions_path, session_id)

    # expects session id
    # returns corresponding directory path for data
    @staticmethod
    def get_session_data_path(session_id):
        session_path = DiskStorageMisc.get_session_path(session_id)
        return os.path.join(session_path, DiskStorageMisc.data_dir)

    # expects identifier
    # returns corresponding identifier path, optionally creates missing directories, based on root path
    @staticmethod
    def get_identifier_path(identifier, create_sub_dirs=0, root_path=None):
        id_parts = identifier.split('/')
        id_path = ''
        idx = 0
        sub_path = root_path
        for part in id_parts:
            id_path = os.path.join(id_path, part)
            if sub_path is not None:
                sub_path = os.path.join(sub_path, part)
            if create_sub_dirs and root_path is not None and os.path.exists(root_path) and not os.path.exists(sub_path) and idx < len(id_parts)-1:
                os.makedirs(sub_path)
            idx = idx + 1
        return id_path

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
