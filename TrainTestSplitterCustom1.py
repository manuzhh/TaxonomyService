from Storage import Storage
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger


class TrainTestSplitterCustom1:

    split_ratio_key = 'train_test_split_ratio'
    random_state_key = 'train_test_split_random_state'
    corpus_identifier_key = 'corpus_identifier'
    ext_train = '_train'
    ext_test = '_test'

    # expects an identifier for a pandas data frame or optionally the pandas data frame itself
    # splits the corresponding data frame into test and train data frames, according to split_ratio from the session_config, and stores them (new identifier = identifier +'_train' or '_test')
    @staticmethod
    def split_train_test(identifier=None, data_frame=None):
        if data_frame is None:
            data_frame = Storage.load_pd_frame(identifier)
        split_ratio = SessionConfigReader.read_value(TrainTestSplitterCustom1.split_ratio_key)
        if split_ratio > 1:
            split_ratio = 1
        random_state = SessionConfigReader.read_value(TrainTestSplitterCustom1.random_state_key)
        if isinstance(random_state, int):
            train = data_frame.sample(frac=split_ratio, random_state=random_state)
        else:
            train = data_frame.sample(frac=split_ratio)
        test = data_frame.drop(train.index)
        if identifier is None:
            identifier = SessionConfigReader.read_value(TrainTestSplitterCustom1.corpus_identifier_key)
        train_name = identifier+TrainTestSplitterCustom1.ext_train
        test_name = identifier+TrainTestSplitterCustom1.ext_test
        Storage.store_pd_frame(train, train_name)
        Storage.store_pd_frame(test, test_name)
        SessionLogger.log('Split \'' + identifier + '\' (' + str(len(data_frame.index)) + ' entries) into \'' + train_name + '\' (' + str(len(train.index)) + ' entries) and \'' + test_name + '\' (' + str(len(test.index)) + ' entries).')
