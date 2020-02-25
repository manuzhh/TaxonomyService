from Storage import Storage
from ConfigReader import ConfigReader
from SessionConfigReader import SessionConfigReader
from datetime import datetime
import pandas as pd


class EvaluationHandler:

    evaluations_id = 'evaluations'
    timestamp_col = 'timestamp'
    session_id_col = 'session id'
    config_id_col = 'config id'
    score_col = 'score'

    additional_columns = [
        'corpus_identifier',
        'preprocessor',
        'vectorizer',
        'word2vec_size',
        'word2vec_window',
        'word2vec_min_count',
        'word-vec_to_doc-vec',
        'classifier',
        'keras_nn_layers',
        'keras_nn_loss',
        'keras_nn_optimizer',
        'keras_nn_metrics',
        'keras_nn_epochs',
        'classification_interpreter',
        'similarity_function'
    ]

    # expects an evaluation score, optionally a session id
    # adds evaluation score to session's evaluations
    @staticmethod
    def add_evaluation(score, session_id=None):
        if session_id is None:
            session_id = ConfigReader.get_session_id()
        config_id = ConfigReader.get_config_id()
        evaluation_frame = Storage.load_pd_frame(EvaluationHandler.evaluations_id, session_id=session_id)
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        evaluation_frame.at[len(evaluation_frame), EvaluationHandler.timestamp_col] = timestamp_str
        evaluation_frame.at[len(evaluation_frame), EvaluationHandler.session_id_col] = session_id
        evaluation_frame.at[len(evaluation_frame), EvaluationHandler.config_id_col] = config_id
        evaluation_frame.at[len(evaluation_frame), EvaluationHandler.score_col] = score
        Storage.store_pd_frame(evaluation_frame, EvaluationHandler.evaluations_id, session_id=session_id)

    # optionally expects a session id
    # returns pandas data frame containing evaluations for session id or current session
    @staticmethod
    def load_evaluations(session_id=None):
        return Storage.load_pd_frame(EvaluationHandler.evaluations_id, session_id=session_id)

    # optionally expects a session id
    # clears evaluations for session id or current session
    @staticmethod
    def clear_evaluations(session_id=None):
        Storage.delete_pd_frame(EvaluationHandler.evaluations_id, session_id=session_id)

    # optionally expects a list of session ids and/or lists for columns to add and/or to remove
    # returns a sorted evaluations data frame, including all specified session and including additional columns, containing some info from the configs
    @staticmethod
    def compare_evaluations(session_ids=None, remove_cols=None, add_cols=None):
        all_evals = pd.DataFrame()

        if session_ids is None:
            all_evals = EvaluationHandler.load_evaluations()
        else:
            for session_id in session_ids:
                all_evals = all_evals.concat(EvaluationHandler.load_evaluations(session_id=session_id), sort=False, ignore_index=True)

        all_evals = all_evals.sort_values(by=[EvaluationHandler.score_col], ascending=False)

        i = 0
        while i < len(all_evals):
            session_id = all_evals.at[i, EvaluationHandler.session_id_col]
            conf_id = all_evals.at[i, EvaluationHandler.config_id_col]
            conf = SessionConfigReader.get_config(session_id=session_id, config_id=conf_id)
            idx = 0
            for key in EvaluationHandler.additional_columns:
                if key in conf:
                    value = conf[key][0]
                else:
                    value = ''
                if key not in all_evals:
                    all_evals[key] = ''
                all_evals.at[idx, key] = value
                idx = idx + 1
            i = i + 1

        if remove_cols is not None:
            for key in remove_cols:
                if key in all_evals:
                    all_evals = all_evals.drop(columns=[key])

        if add_cols is not None:
            i = 0
            while i < len(all_evals):
                session_id = all_evals.at[i, EvaluationHandler.session_id_col]
                conf_id = all_evals.at[i, EvaluationHandler.config_id_col]
                conf = SessionConfigReader.get_config(session_id=session_id, config_id=conf_id)
                idx = 0
                for key in add_cols:
                    if key in conf:
                        value = conf[key][0]
                    else:
                        value = ''
                    if key not in all_evals:
                        all_evals[key] = ''
                    all_evals.at[idx, key] = value
                    idx = idx + 1
                i = i + 1

        return all_evals

    # sorts the stored evaluations data frame by rank (descending)
    @staticmethod
    def sort(session_id=None):
        evals = EvaluationHandler.load_evaluations(session_id=session_id)
        evals = evals.sort_values(by=[EvaluationHandler.score_col], ascending=False)
        Storage.store_pd_frame(evals, EvaluationHandler.evaluations_id, session_id=session_id)

    # sets the currently best performing config, based on the evaluations
    @staticmethod
    def set_best_performing(eval_session_id=None):
        evals = EvaluationHandler.load_evaluations(session_id=eval_session_id)
        evals.sort_values(by=[EvaluationHandler.score_col], ascending=False)
        if evals.size > 0:
            session_id = evals.at[0, EvaluationHandler.session_id_col]
            config_id = evals.at[0, EvaluationHandler.config_id_col]
            SessionConfigReader.set_best_performing_by_ids(session_id=session_id, config_id=config_id)
        else:
            SessionConfigReader.set_best_performing_by_ids()
