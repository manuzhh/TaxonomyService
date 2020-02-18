import pandas as pd
import os.path
import csv
from Storage import Storage
from SessionLogger import SessionLogger
from CategoryListHandler import CategoryListHandler
from SessionConfigReader import SessionConfigReader


class TenKGnadImporter():

    sessions_folder = 'sessions'
    corpus_id_key = 'corpus_identifier'
    csv_ext = '.csv'
    category_name = 'categories'
    text_name = 'text'

    # expects TenKGnad csv path on disk
    # stores content from TenKGnad csv in a pandas data frame in the storage system
    # returns identifier of pandas data frame in storage system, with data frame containing a column 'category' and a column 'text'
    @staticmethod
    def import_docs(csv_path=None):
        if csv_path is None:
            csv_path = TenKGnadImporter.sessions_folder + '.' + SessionConfigReader.get_session_id() + '.' + SessionConfigReader.read_value(TenKGnadImporter.corpus_id_key) + TenKGnadImporter.csv_ext
        df = pd.read_csv(csv_path, sep=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL, header=None, names=[TenKGnadImporter.category_name, TenKGnadImporter.text_name])
        category_list = df[TenKGnadImporter.category_name].tolist()
        df[TenKGnadImporter.category_name] = df.apply(lambda x: [x[TenKGnadImporter.category_name]], axis=1)
        head, f_name = os.path.split(csv_path)
        identifier = f_name.split('.')[0]
        Storage.store_pd_frame(df, identifier)
        SessionLogger.log('TenKGnad Corpus (' + str(len(df.index)) + ' entries) has been imported into \'' + identifier + '\' (columns: \'' + TenKGnadImporter.category_name + '\', \'' + TenKGnadImporter.text_name + '\')')
        category_set = set(category_list)
        category_list = list(category_set)
        CategoryListHandler.set_categories(category_list)
        return identifier
