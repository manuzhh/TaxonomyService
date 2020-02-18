import os.path
import json
from SessionConfigReader import SessionConfigReader
from DiskStorageMisc import DiskStorageMisc


class DiskStorageStopwordHandler:

    stpw_id_key = 'stopwords_identifier'
    file_name = SessionConfigReader.read_value(stpw_id_key) + '.json'
    sw_list_key = 'stopwords'

    # expects a session id
    # returns a string set of the current categories for the specified session
    @staticmethod
    def read_stopwords(session_id):
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        stopwords_path = os.path.join(data_path, DiskStorageStopwordHandler.file_name)
        if not os.path.exists(stopwords_path):
            return set()
        with open(stopwords_path, encoding='utf8') as json_file:
            file = json.load(json_file)
            return set(file[DiskStorageStopwordHandler.sw_list_key])

    # expects a session id and a string set of stopwords
    # sets the session's stopwords
    @staticmethod
    def set_stopwords(session_id, stopwords):
        data = {DiskStorageStopwordHandler.sw_list_key: []}
        for stopword in stopwords:
            data[DiskStorageStopwordHandler.sw_list_key].append(stopword)
        data_path = DiskStorageMisc.get_session_data_path(session_id)
        stopwords_path = os.path.join(data_path, DiskStorageStopwordHandler.file_name)
        DiskStorageMisc.create_data_folder(session_id)
        with open(stopwords_path, 'w+', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

    # expects a session id and a string set of stopwords
    # adds stopwords to the session's stopwords
    @staticmethod
    def add_stopwords(session_id, stopwords):
        current_sw = DiskStorageStopwordHandler.read_stopwords(session_id)
        new_stopwords = current_sw.union(stopwords)
        DiskStorageStopwordHandler.set_stopwords(session_id, new_stopwords)
