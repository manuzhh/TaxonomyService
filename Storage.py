from DiskStorage import DiskStorage
from ConfigReader import ConfigReader


class Storage:

    database_type_key = 'database-type'
    session_id_key = 'session-id'
    db_type_fs = 'filesystem'

    # expects pandas data frame and identifier, optionally a session id
    # stores pandas data frame in storage system
    @staticmethod
    def store_pd_frame(data_frame, identifier, session_id=None):
        db_type = ConfigReader.get_db_type()
        if session_id is None:
            session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.store_pd_frame(data_frame, identifier, session_id)

    # expects identifier, optionally a session id
    # returns corresponding pandas data frame
    @staticmethod
    def load_pd_frame(identifier, session_id=None):
        db_type = ConfigReader.get_db_type()
        if session_id is None:
            session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            return DiskStorage.load_pd_frame(identifier, session_id)

    # expects identifier, optionally a session id
    # deletes corresponding pandas data frame from storage system
    @staticmethod
    def delete_pd_frame(identifier, session_id=None):
        db_type = ConfigReader.get_db_type()
        if session_id is None:
            session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.delete_pd_frame(identifier, session_id)

    # expects model and identifier
    # stores model in storage system
    @staticmethod
    def store_model(model, identifier):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.store_model(model, identifier, session_id)

    # expects identifier
    # returns corresponding model
    @staticmethod
    def load_model(identifier):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            return DiskStorage.load_model(identifier, session_id)

    # expects identifier
    # deletes corresponding model from storage system
    @staticmethod
    def delete_model(identifier):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.delete_model(identifier, session_id)

    # expects model and identifier
    # stores model in storage system
    @staticmethod
    def store_h5_model(model, identifier):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.store_h5_model(model, identifier, session_id)

    # expects identifier
    # returns corresponding model
    @staticmethod
    def load_h5_model(identifier):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            return DiskStorage.load_h5_model(identifier, session_id)

    # expects identifier
    # deletes corresponding model from storage system
    @staticmethod
    def delete_h5_model(identifier):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.delete_h5_model(identifier, session_id)

    # deletes all data from session
    @staticmethod
    def delete_session_data():
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == Storage.db_type_fs:
            DiskStorage.delete_session_data(session_id)
