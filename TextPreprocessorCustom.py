from NoiseRemover import NoiseRemover
from StopWordRemover import StopWordRemover
from Lemmatizer import Lemmatizer
from Storage import Storage
from SessionLogger import SessionLogger


class TextPreprocessorCustom:

    col_name = 'text'
    col_name_noise_removed = 'noise removed'
    col_name_stops_removed = 'stopwords removed'
    col_name_lemmatized = 'lemmatized'
    col_name_preprocessed = 'preprocessed'
    ext_noise_removed = '_noiseRemoved'
    ext_stops_removed = '_stopwordsRemoved'
    ext_lemmatized = '_lemmatized'
    ext_preprocessed = '_preprocessed'

    # expects pandas data frame
    # calls preprocessing functions which perform preprocessing on col_name inside the data frame, optionally stores new data frames in storage system if name was specified and storage_level>=0
    # returns pandas data frame with added column(s) for processed texts
    @staticmethod
    def preprocess_texts(data_frame, col_name=col_name, new_col_name=col_name_preprocessed, storage_level=0, storage_name='', log=1):

        storage_name_ext = storage_name
        if storage_name != '':
            storage_name_ext = storage_name + TextPreprocessorCustom.ext_noise_removed
        noise_removed_df = NoiseRemover.remove_noise(data_frame, col_name=col_name, storage_level=storage_level-1, storage_name=storage_name_ext, log=log)
        if storage_name != '':
            storage_name_ext = storage_name + TextPreprocessorCustom.ext_stops_removed
        stops_removed_df = StopWordRemover.remove_stopwords(noise_removed_df, col_name=TextPreprocessorCustom.col_name_noise_removed, storage_level=storage_level-1, storage_name=storage_name_ext, log=log)
        if storage_name != '':
            storage_name_ext = storage_name + TextPreprocessorCustom.ext_lemmatized
        processed_texts_df = Lemmatizer.normalize(stops_removed_df, col_name=TextPreprocessorCustom.col_name_stops_removed, storage_level=storage_level-1, storage_name=storage_name_ext, log=log)

        if storage_level <= 1:
            processed_texts_df = processed_texts_df.drop(columns=[TextPreprocessorCustom.col_name_noise_removed])
            processed_texts_df = processed_texts_df.drop(columns=[TextPreprocessorCustom.col_name_stops_removed])

        processed_texts_df = processed_texts_df.rename(columns={TextPreprocessorCustom.col_name_lemmatized: new_col_name})

        log_text = 'Documents have been preprocessed (' + str(len(data_frame.index)) + ' entries).'

        if storage_level >= 1 and storage_name != '':
            Storage.store_pd_frame(processed_texts_df, storage_name+TextPreprocessorCustom.ext_preprocessed)
            log_text = log_text + ' Stored in \'' + storage_name + TextPreprocessorCustom.ext_preprocessed + '\' (column: \'' + new_col_name + '\').'

        if log:
            SessionLogger.log(log_text)

        return processed_texts_df
