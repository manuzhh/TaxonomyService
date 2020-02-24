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

    # expects an evaluation score, optionally a session id
    # adds evaluation score to session's evaluations
    @staticmethod
    def add_evaluation(score, session_id=None):
        if session_id is None:
            session_id = ConfigReader.get_session_id()
        config_id = ConfigReader.get_config_id()
        evaluation_frame = Storage.load_pd_frame(EvaluationHandler.evaluations_id, session_id=session_id)
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entries = pd.DataFrame([[timestamp_str, session_id, config_id, score]], columns=[EvaluationHandler.timestamp_col, EvaluationHandler.session_id_col, EvaluationHandler.config_id_col, EvaluationHandler.score_col])
        evaluation_frame = evaluation_frame.append(new_entries, sort=False)
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

    # optionally expects a list of session ids
    # returns a pandas frame with (a) colum(s), containing the test data with the highest score
    @staticmethod
    def compare_evaluations(session_ids=None):
        all_evals = pd.DataFrame()
        if session_ids is None:
            all_evals = EvaluationHandler.load_evaluations()
        else:
            for session_id in session_ids:
                all_evals = all_evals.append(EvaluationHandler.load_evaluations(session_id=session_id), sort=False)
        highest_score = 0
        res_frame = pd.DataFrame()
        for index, row in all_evals.iterrows():
            score = row[EvaluationHandler.score_col]
            if score >= highest_score:
                res_timestamp = row[EvaluationHandler.timestamp_col]
                res_session_id = row[EvaluationHandler.session_id_col]
                res_conf_id = row[EvaluationHandler.config_id_col]
                new_rank_frame = pd.DataFrame([[res_timestamp, res_session_id, res_conf_id, score]], columns=[EvaluationHandler.timestamp_col, EvaluationHandler.session_id_col, EvaluationHandler.config_id_col, EvaluationHandler.score_col])
                if score > highest_score:
                    res_frame = pd.DataFrame()
                res_frame = res_frame.append(new_rank_frame, sort=False)
                highest_score = score
        return res_frame

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
            session_id = evals.at[0, EvaluationHandler.session_id_col][0]
            config_id = evals.at[0, EvaluationHandler.config_id_col][0]
            SessionConfigReader.set_best_performing_by_ids(session_id=session_id, config_id=config_id)
        else:
            SessionConfigReader.set_best_performing_by_ids()
