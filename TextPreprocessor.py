import pandas as pd
from TextPreprocessorCustom import TextPreprocessorCustom
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger


class TextPreprocessor:

    col_name = 'text'
    new_col_name = 'preprocessed'
    preprocessor_key = 'preprocessor'
    preprocessor_custom = 'custom'

    # expects pandas data frame
    # calls preprocessing functions which perform preprocessing on col_name inside the data frame, optionally stores new data frames in storage system if name was specified and storage_level>=0
    # returns pandas data frame with added column(s) for processed texts
    @staticmethod
    def preprocess_texts(data_frame, col_name=col_name, new_col_name=new_col_name, storage_level=0, storage_name='', log=1):
        preprocessor_type = SessionConfigReader.read_value(TextPreprocessor.preprocessor_key)
        if preprocessor_type == TextPreprocessor.preprocessor_custom:
            return TextPreprocessorCustom.preprocess_texts(data_frame, col_name=col_name, new_col_name=new_col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            if log:
                SessionLogger.log('Tried to preprocess texts. Specified Preprocessor is not supported.', log_type='error')
            return pd.DataFrame()
