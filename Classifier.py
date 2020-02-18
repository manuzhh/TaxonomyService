import pandas as pd
from SessionLogger import SessionLogger
from SessionConfigReader import SessionConfigReader
from ClassifierKerasNN import ClassifierKerasNN


class Classifier:

    classifier_key = 'classifier'
    classifier_keras_nn = 'keras_nn'
    fv_col_name = 'document vector'
    cat_v_col_name = 'categories vector'
    class_out_col_name = 'classification output'

    # expects pandas data frame, optionally an identifier for the model to train and column names referencing the vectors used for training
    # returns the model identifier
    @staticmethod
    def train_model(data_frame, model_id=None, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name):
        classifier_type = SessionConfigReader.read_value(Classifier.classifier_key)
        if classifier_type == Classifier.classifier_keras_nn:
            return ClassifierKerasNN.train_model(data_frame, model_id=model_id, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name)
        else:
            SessionLogger.log('Tried to train classifier model. Specified Classifier is not supported.', log_type='error')
            return ''

    # expects pandas data frame, optionally an identifier for the new model and column names referencing the vectors used for training
    # creates a neural network model and trains the model with the vectors from the the data frame
    # returns the identifier of the new model
    @staticmethod
    def create_model(data_frame, new_model_id=None, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name):
        classifier_type = SessionConfigReader.read_value(Classifier.classifier_key)
        if classifier_type == Classifier.classifier_keras_nn:
            return ClassifierKerasNN.create_model(data_frame, new_model_id=new_model_id, fv_col_name=fv_col_name, cat_v_col_name=cat_v_col_name)
        else:
            SessionLogger.log('Tried to create classifier model. Specified Classifier is not supported.', log_type='error')
            return ''

    # expects pandas data frame
    # adds a column to the data frame, containing the classification output
    # returns expanded data frame
    @staticmethod
    def classify(data_frame, model_id=None, col_name=fv_col_name, new_col_name=class_out_col_name, storage_level=0, storage_name='', log=1):
        classifier_type = SessionConfigReader.read_value(Classifier.classifier_key)
        if classifier_type == Classifier.classifier_keras_nn:
            return ClassifierKerasNN.classify(data_frame, model_id=model_id, col_name=col_name, new_col_name=new_col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            if log:
                SessionLogger.log('Tried to classify data. Specified Classifier is not supported.', log_type='error')
            return pd.DataFrame()
