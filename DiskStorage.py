import pandas as pd
import os.path
import os
import shutil
from gensim.models import Word2Vec
from keras.models import load_model
from SessionLogger import SessionLogger


class DiskStorage:

    sessions_dir = 'sessions'
    data_dir = 'data'
    preprocess_dir = 'import_and_preprocess'
    vectorize_dir = 'vectorize'
    pickle_ext = '.pickle'
    model_ext = '.model'
    h5_model_ext = '.h5'

    # expects session id
    # returns corresponding directory path for data
    @staticmethod
    def get_session_data_path(session_id):
        #sessions_path = os.path.join('..', DiskStorage.sessions_dir)
        sessions_path = DiskStorage.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        return os.path.join(session_path, DiskStorage.data_dir)

    # expects identifier and session identifier
    # returns corresponding file path
    @staticmethod
    def get_file_path_pickle(identifier, session_id):
        data_path = DiskStorage.get_session_data_path(session_id)
        return os.path.join(data_path, identifier + DiskStorage.pickle_ext)

    # expects identifier and session identifier
    # returns corresponding file path
    @staticmethod
    def get_file_path_model(identifier, session_id):
        data_path = DiskStorage.get_session_data_path(session_id)
        return os.path.join(data_path, identifier + DiskStorage.model_ext)

    # expects identifier and session identifier
    # returns corresponding file path
    @staticmethod
    def get_file_path_h5_model(identifier, session_id):
        data_path = DiskStorage.get_session_data_path(session_id)
        return os.path.join(data_path, identifier + DiskStorage.h5_model_ext)

    # expects pandas data frame, data frame identifier and session identifier
    # stores pandas data frame on disk with specified data frame identifier as name
    @staticmethod
    def store_pd_frame(data_frame, identifier, session_id):
        data_frame.to_pickle(DiskStorage.get_file_path_pickle(identifier, session_id))

    # expects identifier and session identifier
    # returns corresponding pandas data frame
    @staticmethod
    def load_pd_frame(identifier, session_id):
        return pd.read_pickle(DiskStorage.get_file_path_pickle(identifier, session_id))

    # expects identifier and session identifier
    # deletes corresponding pandas data frame from disk
    @staticmethod
    def delete_pd_frame(identifier, session_id):
        path = DiskStorage.get_file_path_pickle(identifier, session_id)
        if os.path.exists(path):
            os.remove(path)
            SessionLogger.log('Data frame \'' + identifier + '\' has been deleted.')

    # expects path to folder
    # deletes all files from folder
    @staticmethod
    def delete_from_folder(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # expects session identifier
    # deletes all data from session
    @staticmethod
    def delete_session_data(session_id):
        folder = DiskStorage.get_session_data_path(session_id)
        DiskStorage.delete_from_folder(folder)
        SessionLogger.log('All session data has been deleted.')

    # model, model identifier and session identifier
    # stores model on disk with specified model identifier as name
    @staticmethod
    def store_model(model, identifier, session_id):
        model.save(DiskStorage.get_file_path_model(identifier, session_id))

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
        model.save(DiskStorage.get_file_path_h5_model(identifier, session_id))

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

    # # expects session identifier
    # # deletes preprocessing data from session
    # @staticmethod
    # def delete_session_preprocess_data(session_id):
    #     data_folder = DiskStorage.get_session_data_path(session_id)
    #     preprocess_folder = os.path.join(data_folder, DiskStorage.preprocess_dir)
    #     DiskStorage.delete_from_folder(preprocess_folder)
    #
    # # expects session identifier
    # # deletes preprocessing data from session
    # @staticmethod
    # def delete_session_vectorize_data(session_id):
    #     data_folder = DiskStorage.get_session_data_path(session_id)
    #     vectorize_folder = os.path.join(data_folder, DiskStorage.vectorize_dir)
    #     DiskStorage.delete_from_folder(vectorize_folder)
