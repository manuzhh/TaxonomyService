from ConfigReader import ConfigReader
from DiskStorageCategoryListHandler import DiskStorageCategoryListHandler
from SessionLogger import SessionLogger


class CategoryListHandler:

    db_type_fs = 'filesystem'

    # returns a string list of the session's current categories
    @staticmethod
    def read_categories():
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == CategoryListHandler.db_type_fs:
            return DiskStorageCategoryListHandler.read_categories(session_id)
        else:
            return list()

    # expects a string list of categories
    # sets the session's categories
    @staticmethod
    def set_categories(categories):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == CategoryListHandler.db_type_fs:
            DiskStorageCategoryListHandler.set_categories(session_id, categories)
            SessionLogger.log(str(len(categories)) + ' categories have been set.')

    # expects a string list of stopwords
    # adds categories to the session's categories (appending at the end)
    @staticmethod
    def add_categories(categories):
        db_type = ConfigReader.get_db_type()
        session_id = ConfigReader.get_session_id()
        if db_type == CategoryListHandler.db_type_fs:
            DiskStorageCategoryListHandler.add_categories(session_id, categories)
            SessionLogger.log(str(len(categories)) + ' categories have been added.')
