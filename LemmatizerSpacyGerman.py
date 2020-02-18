from Storage import Storage
from SessionLogger import SessionLogger
import spacy

model_name = 'de_core_news_md'
model = spacy.load(model_name)


class LemmatizerSpacyGerman:

    col_name = 'text'
    new_col_name = 'lemmatized'

    # expects a text string
    # lemmatizes words from text string
    # returns lemmatized string
    @staticmethod
    def process_text(text: str):
        words = model(text)
        lem_text = ''
        for word in words:
            lem_text = lem_text + word.lemma_ + ' '
        if len(lem_text) > 0:
            lem_text = lem_text[:-1]
        return lem_text

    # expects pandas data frame and a column name for which words should be lemmatized
    # lemmatizes words from pandas data frame and adds result to a new column called 'lemmatized', optionally stores new data frame with the specified name if storage_level>=1
    # returns new pandas data frame, containing a column 'lemmatized'
    @staticmethod
    def normalize(data_frame, col_name=col_name, storage_level=0, storage_name='', log=1):
        data_frame[LemmatizerSpacyGerman.new_col_name] = data_frame.apply(lambda x: LemmatizerSpacyGerman.process_text(x[col_name]), axis=1)
        log_text = 'Documents lemmatized with spacy (' + str(len(data_frame.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            Storage.store_pd_frame(data_frame, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + LemmatizerSpacyGerman.new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)
        return data_frame
