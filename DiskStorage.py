import pandas as pd
import os.path
import os
from gensim.models import Word2Vec
from keras.models import load_model
from SessionLogger import SessionLogger
from DiskStorageMisc import DiskStorageMisc


class DiskStorage:

    pickle_ext = '.pickle'
    model_ext = '.model'
    h5_model_ext = '.h5'

    # expects identifier and session identifier
    # returns corresponding file path
    @staticmethod
    def get_file_path_pickle(identifier, session_id, create_sub_dirs=0, root_path=None):
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        identifier = DiskStorageMisc.get_identifier_path(identifier, create_sub_dirs=create_sub_dirs, root_path=root_path)
        return os.path.join(data_path, identifier + DiskStorage.pickle_ext)

    # expects identifier and session identifier
    # returns corresponding file path
    @staticmethod
    def get_file_path_model(identifier, session_id, create_sub_dirs=0, root_path=None):
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        identifier = DiskStorageMisc.get_identifier_path(identifier, create_sub_dirs=create_sub_dirs, root_path=root_path)
        return os.path.join(data_path, identifier + DiskStorage.model_ext)

    # expects identifier and session identifier
    # returns corresponding file path
    @staticmethod
    def get_file_path_h5_model(identifier, session_id, create_sub_dirs=0, root_path=None):
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        identifier = DiskStorageMisc.get_identifier_path(identifier, create_sub_dirs=create_sub_dirs, root_path=root_path)
        return os.path.join(data_path, identifier + DiskStorage.h5_model_ext)

    # expects pandas data frame, data frame identifier and session identifier
    # stores pandas data frame on disk with specified data frame identifier as name
    @staticmethod
    def store_pd_frame(data_frame, identifier, session_id):
        DiskStorageMisc.create_data_folder(session_id)
        data_frame.to_pickle(DiskStorage.get_file_path_pickle(identifier, session_id, create_sub_dirs=1, root_path=DiskStorageMisc.get_session_data_path(session_id)))

    # expects identifier and session identifier
    # returns corresponding pandas data frame
    @staticmethod
    def load_pd_frame(identifier, session_id):
        fp = DiskStorage.get_file_path_pickle(identifier, session_id)
        if os.path.isfile(fp):
            return pd.read_pickle(fp)
        else:
            return pd.DataFrame()

    # expects identifier and session identifier
    # deletes corresponding pandas data frame from disk
    @staticmethod
    def delete_pd_frame(identifier, session_id):
        path = DiskStorage.get_file_path_pickle(identifier, session_id)
        if os.path.exists(path):
            os.remove(path)
            SessionLogger.log('Data frame \'' + identifier + '\' has been deleted.')

    # model, model identifier and session identifier
    # stores model on disk with specified model identifier as name
    @staticmethod
    def store_model(model, identifier, session_id):
        DiskStorageMisc.create_data_folder(session_id)
        model.save(DiskStorage.get_file_path_model(identifier, session_id, create_sub_dirs=1, root_path=DiskStorageMisc.get_session_data_path(session_id)))

    # expects identifier and session identifier
    # returns corresponding model
    @staticmethod
    def load_model(identifier, session_id):
        return Word2Vec.load(DiskStorage.get_file_path_model(identifier, session_id))

    # expects identifier and session identifier
    # deletes corresponding model from disk
    @staticmethod
    def delete_model(identifier, session_id):
        path = DiskStorage.get_file_path_model(identifier, session_id)
        if os.path.exists(path):
            os.remove(path)
            SessionLogger.log('Vector Model \'' + identifier + '\' has been deleted.')

    # model, model identifier and session identifier
    # stores model on disk with specified model identifier as name
    @staticmethod
    def store_h5_model(model, identifier, session_id):
        DiskStorageMisc.create_data_folder(session_id)
        model.save(DiskStorage.get_file_path_h5_model(identifier, session_id, create_sub_dirs=1, root_path=DiskStorageMisc.get_session_data_path(session_id)))

    # expects identifier and session identifier
    # returns corresponding model
    @staticmethod
    def load_h5_model(identifier, session_id):
        return load_model(DiskStorage.get_file_path_h5_model(identifier, session_id))

    # expects identifier and session identifier
    # deletes corresponding model from disk
    @staticmethod
    def delete_h5_model(identifier, session_id):
        path = DiskStorage.get_file_path_h5_model(identifier, session_id)
        if os.path.exists(path):
            os.remove(path)
            SessionLogger.log('Classification Model \'' + identifier + '\' has been deleted.')

    # expects path to folder
    # deletes all files from folder
    @staticmethod
    def delete_from_folder(path):
        DiskStorageMisc.delete_from_folder(path)

    # expects session identifier
    # deletes all data from session
    @staticmethod
    def delete_session_data(session_id):
        DiskStorageMisc.delete_session_data(session_id)

