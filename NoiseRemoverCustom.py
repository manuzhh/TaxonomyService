import re
from Storage import Storage
from SessionLogger import SessionLogger


class NoiseRemoverCustom:

    col_name = 'text'
    new_col_name = 'noise removed'

    # expects a text string
    # removes noise from text string
    # returns cleaned string
    @staticmethod
    def process_text(text: str):
        text = text.replace(' - ', '-')
        text = text.replace(' -', '-')
        text = text.replace('- ', '-')
        text = text.replace('-', ' ')
        # Remove punctuations
        text = re.sub(r'[^\w\s]', '', text)
        # remove tags
        text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
        # remove special characters and digits
        text = re.sub("(\\d|\\W)+", " ", text)
        return text

    # expects pandas data frame and a column name for which noise should be removed
    # removes noise from pandas data frame and adds result to a new column called 'noise removed', optionally stores new data frame with the specified name if storage_level>=1
    # returns new pandas data frame, containing a column 'noise removed'
    @staticmethod
    def remove_noise(data_frame, col_name=col_name, storage_level=0, storage_name='', log=1):
        data_frame[NoiseRemoverCustom.new_col_name] = data_frame.apply(lambda x: NoiseRemoverCustom.process_text(x[col_name]), axis=1)
        log_text = 'Removed noise from documents (' + str(len(data_frame.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            Storage.store_pd_frame(data_frame, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + NoiseRemoverCustom.new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)
        return data_frame
