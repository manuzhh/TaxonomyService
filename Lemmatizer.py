import pandas as pd
from LemmatizerSpacyGerman import LemmatizerSpacyGerman
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger


class Lemmatizer:

    col_name = 'text'
    lemmatizer_key = 'lemmatizer'
    lemmatizer_spacy_german = 'spacy-german'

    # expects pandas data frame and a column name for which words should be lemmatized
    # lemmatizes words from pandas data frame and adds result to a new column called 'lemmatized', optionally stores new data frame with the specified name if storage_level>=1
    # returns new pandas data frame, containing a column 'lemmatized'
    @staticmethod
    def normalize(data_frame, col_name=col_name, storage_level=0, storage_name='', log=1):
        lemmatizer = SessionConfigReader.read_value(Lemmatizer.lemmatizer_key)
        if lemmatizer == Lemmatizer.lemmatizer_spacy_german:
            return LemmatizerSpacyGerman.normalize(data_frame, col_name=col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            if log:
                SessionLogger.log('Tried to lemmatize documents. Specified Lemmatizer not supported.', log_type='error')
            return pd.DataFrame()
