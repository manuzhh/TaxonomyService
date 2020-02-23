import os.path
import json
from SessionConfigReader import SessionConfigReader
from DiskStorageMisc import DiskStorageMisc


class DiskStorageCategoryListHandler:

    cat_id_key = 'categories_identifier'
    ext_json = '.json'
    cat_list_key = 'categories'

    # expects a session id
    # returns a string list of the current categories for the specified session
    @staticmethod
    def read_categories(session_id):
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        file_name = SessionConfigReader.read_value(DiskStorageCategoryListHandler.cat_id_key) + DiskStorageCategoryListHandler.ext_json
        categories_path = os.path.join(data_path, file_name)
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
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        file_name = SessionConfigReader.read_value(DiskStorageCategoryListHandler.cat_id_key) + DiskStorageCategoryListHandler.ext_json
        categories_path = os.path.join(data_path, file_name)
        DiskStorageMisc.create_data_folder(session_id)
        with open(categories_path, 'w+', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    # expects a session id and a string list of stopwords
    # adds categories to the session's categories (appending at the end)
    @staticmethod
    def add_categories(session_id, categories):
        current_cats = DiskStorageCategoryListHandler.read_categories(session_id)
        current_cats.extend(categories)
        DiskStorageCategoryListHandler.set_categories(session_id, current_cats)
