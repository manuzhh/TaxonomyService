from CorpusImporter import CorpusImporter
from Storage import Storage
from TextPreprocessor import TextPreprocessor
from StopwordDownloaderNLTK import StopwordDownloaderNLTK
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger
from Vectorizer import Vectorizer
from TrainTestSplitter import TrainTestSplitter
from ClassificationInterpreter import ClassificationInterpreter
from Classifier import Classifier
from EvaluationHandler import EvaluationHandler
from SessionConfigBuilder import SessionConfigBuilder
from ConfigReader import ConfigReader


class SetupRunner:

    column_evaluation_score = 'score'
    corpus_id_key = 'corpus_identifier'
    ext_preprocessed = '_preprocessed'
    ext_vectorized = '_vectorized'
    vec_model_id_key = 'vec_model_id'
    keras_nn_model_id_key = 'keras_nn_model_id'
    ext_train = '_train'
    ext_test = '_test'
    column_score = 'score'

    # runs the setup routine (fully or partly)
    @staticmethod
    def run_setup(run_import=1, run_preprocessing=1, run_vectorization=1, run_classification=1):
        corpus_id = SessionConfigReader.read_value(SetupRunner.corpus_id_key)
        if run_import:
            Storage.delete_session_data()
            SessionLogger.clear()
            identifier = CorpusImporter.import_docs()
            df = Storage.load_pd_frame(identifier)
            StopwordDownloaderNLTK.get_stopwords()
        else:
            df = Storage.load_pd_frame(corpus_id)
        if run_preprocessing:
            df = TextPreprocessor.preprocess_texts(df, storage_level=1, storage_name=corpus_id)
        else:
            df = Storage.load_pd_frame(corpus_id+SetupRunner.ext_preprocessed)
        if run_vectorization:
            Storage.delete_model(SessionConfigReader.read_value(SetupRunner.vec_model_id_key))
            Vectorizer.create_model(df)
            df = Vectorizer.vectorize(df, storage_level=1, storage_name=corpus_id)
        else:
            df = Storage.load_pd_frame(corpus_id+SetupRunner.ext_vectorized)
        if run_classification:
            Storage.delete_h5_model(SessionConfigReader.read_value(SetupRunner.keras_nn_model_id_key))
            df = ClassificationInterpreter.create_out_vectors(df, storage_level=1, storage_name=corpus_id)
            Classifier.create_model(df)

    # runs a single test with the current config settings
    # returns a data frame, containing the results
    @staticmethod
    def run_classification_test():
        Storage.delete_h5_model(SessionConfigReader.read_value(SetupRunner.keras_nn_model_id_key))
        corpus_id = SessionConfigReader.read_value(SetupRunner.corpus_id_key)
        vectorized_df_id = corpus_id + SetupRunner.ext_vectorized
        vectorized_df = Storage.load_pd_frame(vectorized_df_id)
        TrainTestSplitter.split_train_test(identifier=vectorized_df_id, data_frame=vectorized_df)
        train_df_id = vectorized_df_id + SetupRunner.ext_train
        train = Storage.load_pd_frame(train_df_id)
        test_df_id = vectorized_df_id + SetupRunner.ext_test
        test = Storage.load_pd_frame(test_df_id)
        train_classification_outs = ClassificationInterpreter.create_out_vectors(train)
        Classifier.create_model(train_classification_outs)
        test_classified = Classifier.classify(test)
        test_interpreted = ClassificationInterpreter.interpret_output(test_classified)
        score = ClassificationInterpreter.evaluate_output(test_interpreted)
        EvaluationHandler.add_evaluation(score)
        return test_interpreted

    # runs config tests
    # returns an evaluation frame
    @staticmethod
    def run_config_tests(run_import=0, run_preprocessing=0, run_vectorization=0, config_ids=None, resume_at_idx=0):
        if config_ids is None:
            config_ids = SessionConfigBuilder.create_session_configs()
        n_configs = len(config_ids)
        idx = resume_at_idx
        while idx < len(config_ids):
            config_id = config_ids[idx]
            ConfigReader.set_session_config_id(config_id)

            SetupRunner.run_setup(run_import=run_import, run_preprocessing=run_preprocessing, run_vectorization=run_vectorization, run_classification=0)

            res = SetupRunner.run_classification_test()

            score = ClassificationInterpreter.evaluate_output(res)

            corpus_id = SessionConfigReader.read_value(SetupRunner.corpus_id_key)
            vectorized_df_id = corpus_id + SetupRunner.ext_vectorized
            train_df_id = vectorized_df_id + SetupRunner.ext_train
            test_df_id = vectorized_df_id + SetupRunner.ext_test
            Storage.delete_pd_frame(train_df_id)
            Storage.delete_pd_frame(test_df_id)

            idx = idx + 1
            SessionLogger.log('Evaluated config # ' + str(idx) + ' / ' + str(n_configs) + ' . Score: ' + str(score))
        EvaluationHandler.sort()
        evaluations = EvaluationHandler.load_evaluations()
        return evaluations

    # expects a list of config_ids
    # returns the list, sorted by config id values
    @staticmethod
    def sort_config_list(config_list):
        conf_name = SessionConfigBuilder.get_configs_name()
        idx_list = list()
        for conf in config_list:
            conf_idx = conf.split(conf_name)[1]
            idx_list.append(int(conf_idx))
        idx_list.sort()
        sorted_configs = list()
        for idx in idx_list:
            sorted_configs.append(conf_name + str(idx))
        return sorted_configs

    # expects an index (idx=1 represents the first file)
    # resumes config tests at index
    @staticmethod
    def resume_config_tests_at_idx(idx, run_import=0, run_preprocessing=0, run_vectorization=0):
        SessionLogger.log('Resuming config tests at config # ' + str(idx) + ' ...')
        if idx > 0:
            idx = idx - 1
        configs_location = SessionConfigBuilder.get_configs_location()
        config_ids = Storage.list_ids(configs_location)
        config_ids = SetupRunner.sort_config_list(config_ids)
        config_ids_with_dir = list()
        for c_id in config_ids:
            config_ids_with_dir.append(configs_location + '/' + c_id)
        SessionLogger.log('Config ID list has been restored.')
        return SetupRunner.run_config_tests(run_import=run_import, run_preprocessing=run_preprocessing, run_vectorization=run_vectorization, config_ids=config_ids_with_dir, resume_at_idx=idx)
