import pandas as pd
from StopWordRemoverCustom import StopWordRemoverCustom
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger


class StopWordRemover:

    col_name = 'text'
    stopwordremover_key = 'stopword_remover'
    custom_sw_key = 'additional_stopwords'
    stopwordremover_custom = 'custom'

    # expects pandas data frame, optionally a column name for which stopwords should be removed, optionally a custom stopwords list
    # removes stopwords from pandas data frame and adds result to a new column called 'stopwords removed', optionally stores new data frame with the specified name if storage_level>=1
    # returns new pandas data frame, containing a column 'stopwords removed'
    @staticmethod
    def remove_stopwords(data_frame, custom_stop_words=None, download_live_stopwords=0, col_name=col_name, storage_level=0, storage_name='', log=1):
        stopwordremover = SessionConfigReader.read_value(StopWordRemover.stopwordremover_key)
        custom_stop_words = custom_stop_words + SessionConfigReader.read_value(StopWordRemover.custom_sw_key).split()
        if stopwordremover == StopWordRemover.stopwordremover_custom:
            return StopWordRemoverCustom.remove_stopwords(data_frame, custom_stop_words=custom_stop_words, download_live_stopwords=download_live_stopwords, col_name=col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            if log:
                SessionLogger.log('Tried to remove stopwords from documents. Specified Stopword Remover not supported.', log_type='error')
            return pd.DataFrame()

    # returns set of stopwords
    @staticmethod
    def get_stopwords():
        stopwordremover = SessionConfigReader.read_value(StopWordRemover.stopwordremover_key)
        if stopwordremover == StopWordRemover.stopwordremover_custom:
            return StopWordRemoverCustom.get_stopwords()
        else:
            return set()
