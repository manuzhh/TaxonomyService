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
            df = TextPreprocessor.preprocess_texts(df)
        else:
            df = Storage.load_pd_frame(corpus_id+SetupRunner.ext_preprocessed)
        if run_vectorization:
            Storage.delete_model(SessionConfigReader.read_value(SetupRunner.vec_model_id_key))
            Vectorizer.create_model(df)
            df = Vectorizer.vectorize(df)
        else:
            df = Storage.load_pd_frame(corpus_id+SetupRunner.ext_vectorized)
        if run_classification:
            Storage.delete_h5_model(SessionConfigReader.read_value(SetupRunner.keras_nn_model_id_key))
            df = ClassificationInterpreter.create_out_vectors(df)
            Classifier.create_model(df)

    # runs config tests
    # returns an evaluation frame
    @staticmethod
    def run_config_tests(run_import=0, run_preprocessing=0, run_vectorization=0):
        config_ids = SessionConfigBuilder.create_session_configs()
        n_configs = len(config_ids)
        idx = 0
        for config_id in config_ids:
            ConfigReader.set_config(config_id)
            corpus_id = SessionConfigReader.read_value(SetupRunner.corpus_id_key)
            SetupRunner.run_setup(run_import=run_import, run_preprocessing=run_preprocessing, run_vectorization=run_vectorization, run_classification=0)
            Storage.delete_h5_model(SessionConfigReader.read_value(SetupRunner.keras_nn_model_id_key))
            vectorized_df_id = corpus_id + SetupRunner.ext_vectorized
            df = Storage.load_pd_frame(vectorized_df_id)
            TrainTestSplitter.split_train_test(df)
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
            idx = idx + 1
            SessionLogger.log('Evaluated config # ' + str(idx) + ' / ' + str(n_configs) + ' .')
        evaluations = EvaluationHandler.load_evaluations()
        evaluations.sort_values(by=[SetupRunner.column_score])
        return evaluations
