from Storage import Storage
from SessionLogger import SessionLogger
from StopwordDownloaderNLTK import StopwordDownloaderNLTK
from StopwordHandler import StopwordHandler


class StopWordRemoverCustom:

    col_name = 'text'
    new_col_name = 'stopwords removed'
    german = 'german'

    # expects list of words
    # returns list of words, expanded by capitalized versions of each word
    @staticmethod
    def capitalize_words(words):
        words_new = set()
        for word in words:
            words_new.add(word)
            words_new.add(word.capitalize())
        return words_new

    # expects a text string and a list of stopwords
    # removes stopwords from text string
    # returns cleaned string
    @staticmethod
    def process_text(text: str, stop_words):
        cleaned_text = ''
        words = text.split()
        for word in words:
            if word not in stop_words:
                cleaned_text = cleaned_text + word + ' '
        if len(cleaned_text) > 0:
            cleaned_text = cleaned_text[:-1]
        return cleaned_text

    # expects pandas data frame, optionally a column name for which stopwords should be removed, optionally a custom stopwords list
    # removes stopwords from pandas data frame and adds result to a new column called 'stopwords removed', optionally stores new data frame with the specified name if storage_level>=1
    # returns new pandas data frame, containing a column 'stopwords removed'
    @staticmethod
    def remove_stopwords(data_frame, custom_stop_words=None, download_live_stopwords=0, col_name=col_name, storage_level=0, storage_name='', log=1):
        df = data_frame.copy()
        stop_words = StopwordHandler.read_stopwords()
        if download_live_stopwords:
            stop_words = stop_words.union(StopwordDownloaderNLTK.get_stopwords(store=0))
        stop_words = StopWordRemoverCustom.capitalize_words(stop_words)
        if custom_stop_words is not None:
            stop_words = stop_words.union(custom_stop_words)
        df[StopWordRemoverCustom.new_col_name] = df.apply(lambda x: StopWordRemoverCustom.process_text(x[col_name], stop_words), axis=1)
        log_text = 'Removed stop words from documents (' + str(len(df.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            Storage.store_pd_frame(df, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + StopWordRemoverCustom.new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)
        return df

    # returns set of stopwords
    @staticmethod
    def get_stopwords():
        return StopwordHandler.read_stopwords()
