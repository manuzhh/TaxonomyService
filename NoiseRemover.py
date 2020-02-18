import pandas as pd
from NoiseRemoverCustom import NoiseRemoverCustom
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger


class NoiseRemover:

    col_name = 'text'
    noiseremover_key = 'noise_remover'
    noiseremover_custom = 'custom'

    # expects pandas data frame and a column name for which noise should be removed
    # removes noise from pandas data frame and adds result to a new column called 'noise removed', optionally stores new data frame with the specified name if storage_level>=1
    # returns new pandas data frame, containing a column 'noise removed'
    @staticmethod
    def remove_noise(data_frame, col_name=col_name, storage_level=0, storage_name='', log=1):
        noiseremover_type = SessionConfigReader.read_value(NoiseRemover.noiseremover_key)
        if noiseremover_type == NoiseRemover.noiseremover_custom:
            return NoiseRemoverCustom.remove_noise(data_frame, col_name=col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            if log:
                SessionLogger.log('Tried to remove noise from documents. Specified Noise Remover not supported.', log_type='error')
            return pd.DataFrame()
