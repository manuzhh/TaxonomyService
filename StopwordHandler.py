from ConfigReader import ConfigReader
from DiskStorageStopwordHandler import DiskStorageStopwordHandler
from SessionLogger import SessionLogger


class StopwordHandler:

    db_type_fs = 'filesystem'

    # returns a string set of the session's current stopwords
    @staticmethod
    def read_stopwords():
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == StopwordHandler.db_type_fs:
            return DiskStorageStopwordHandler.read_stopwords(session_id)
        else:
            return list()

    # expects a string set of stopwords
    # sets the session's stopwords
    @staticmethod
    def set_stopwords(stopwords):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == StopwordHandler.db_type_fs:
            DiskStorageStopwordHandler.set_stopwords(session_id, stopwords)
            SessionLogger.log(str(len(stopwords)) + ' stop words have been set.')

    # expects a string set of stopwords
    # adds stopwords to the session's stopwords
    @staticmethod
    def add_stopwords(stopwords):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == StopwordHandler.db_type_fs:
            DiskStorageStopwordHandler.add_stopwords(session_id, stopwords)
            SessionLogger.log(str(len(stopwords)) + ' stop words have been added.')
