import os.path
import json
from SessionConfigReader import SessionConfigReader


class DiskStorageCategoryListHandler:

    sessions_dir = 'sessions'
    data_dir = 'data'
    cat_id_key = 'categories_identifier'
    file_name = SessionConfigReader.read_value(cat_id_key) + '.json'
    cat_list_key = 'categories'

    # expects a session id
    # returns a string list of the current categories for the specified session
    @staticmethod
    def read_categories(session_id):
        #sessions_path = os.path.join('..', DiskStorageCategoryListHandler.sessions_dir)
        sessions_path = DiskStorageCategoryListHandler.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        data_path = os.path.join(session_path, DiskStorageCategoryListHandler.data_dir)
        categories_path = os.path.join(data_path, DiskStorageCategoryListHandler.file_name)
        if not os.path.exists(categories_path):
            return list()
        with open(categories_path, encoding='utf8') as json_file:
            file = json.load(json_file)
            return file[DiskStorageCategoryListHandler.cat_list_key]

    # expects a session id and a string list of categories
    # sets the session's categories
    @staticmethod
    def set_categories(session_id, categories):
        data = {DiskStorageCategoryListHandler.cat_list_key: []}
        for category in categories:
            data[DiskStorageCategoryListHandler.cat_list_key].append(category)
        #sessions_path = os.path.join('..', DiskStorageCategoryListHandler.sessions_dir)
        sessions_path = DiskStorageCategoryListHandler.sessions_dir
        session_path = os.path.join(sessions_path, session_id)
        data_path = os.path.join(session_path, DiskStorageCategoryListHandler.data_dir)
        categories_path = os.path.join(data_path, DiskStorageCategoryListHandler.file_name)
        with open(categories_path, 'w+', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    # expects a session id and a string list of stopwords
    # adds categories to the session's categories (appending at the end)
    @staticmethod
    def add_categories(session_id, categories):
        current_cats = DiskStorageCategoryListHandler.read_categories(session_id)
        current_cats.extend(categories)
        DiskStorageCategoryListHandler.set_categories(session_id, current_cats)
