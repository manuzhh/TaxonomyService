from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger
from TrainTestSplitterCustom1 import TrainTestSplitterCustom1


class TrainTestSplitter:

    tt_splitter_key = 'train_test_splitter'
    tt_splitter_custom1 = 'custom1'

    # expects an identifier for a pandas data frame or optionally the pandas data frame itself
    # splits the corresponding data frame into test and train data frames and stores them (new identifier = identifier +'_train' or '_test')
    @staticmethod
    def split_train_test(identifier=None, data_frame=None):
        tt_splitter_type = SessionConfigReader.read_value(TrainTestSplitter.tt_splitter_key)
        if tt_splitter_type == TrainTestSplitter.tt_splitter_custom1:
            TrainTestSplitterCustom1.split_train_test(identifier=identifier, data_frame=data_frame)
        else:
            SessionLogger.log('Tried to split \'' + identifier + '\' into train and test set. Specified TrainTestSplitter is not supported.', log_type='error')
