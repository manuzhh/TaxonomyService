import pandas as pd
from SessionLogger import SessionLogger
from SessionConfigReader import SessionConfigReader
from ClassificationInterpreterCustom1 import ClassificationInterpreterCustom1
from ClassificationInterpreterCustom2 import ClassificationInterpreterCustom2


class ClassificationInterpreter:

    classification_interpreter_key = 'classification_interpreter'
    classification_interpreter_custom1 = 'custom1'
    classification_interpreter_custom2 = 'custom2'
    col_name_categories = 'categories'
    new_col_name_cat_vec = 'categories vector'
    col_name_class_out = 'classification output'
    col_name_result = 'result'

    # expects a pandas data frame, containing a category column
    # creates an output vector for training from each entry in the category column from the data frame and stores it in a new column
    # returns pandas data frame with added column for added output vectors
    @staticmethod
    def create_out_vectors(data_frame, col_name=col_name_categories, new_col_name=new_col_name_cat_vec, storage_level=0, storage_name=''):
        classification_interpreter = SessionConfigReader.read_value(ClassificationInterpreter.classification_interpreter_key)
        if classification_interpreter == ClassificationInterpreter.classification_interpreter_custom1:
            return ClassificationInterpreterCustom1.create_out_vectors(data_frame, col_name=col_name, new_col_name=new_col_name, storage_level=storage_level, storage_name=storage_name)
        elif classification_interpreter == ClassificationInterpreter.classification_interpreter_custom2:
            return ClassificationInterpreterCustom2.create_out_vectors(data_frame, col_name=col_name, new_col_name=new_col_name, storage_level=storage_level, storage_name=storage_name)
        else:
            SessionLogger.log('Tried to create category vectors. Specified ClassificationInterpreter is not supported.', log_type='error')
            return pd.DataFrame()

    # expects a pandas data frame, containing a column with classification output vectors
    # creates a list of categories from each classification output vector and stores it in a new column
    # returns pandas data frame with added column for added category lists
    @staticmethod
    def interpret_output(data_frame, col_name=col_name_class_out, new_col_name=col_name_result, storage_level=0, storage_name='', log=1):
        classification_interpreter = SessionConfigReader.read_value(ClassificationInterpreter.classification_interpreter_key)
        if classification_interpreter == ClassificationInterpreter.classification_interpreter_custom1:
            return ClassificationInterpreterCustom1.interpret_output(data_frame, col_name=col_name, new_col_name=new_col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        elif classification_interpreter == ClassificationInterpreter.classification_interpreter_custom2:
            return ClassificationInterpreterCustom2.interpret_output(data_frame, col_name=col_name, new_col_name=new_col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            SessionLogger.log('Tried to interpret output vectors. Specified ClassificationInterpreter is not supported.', log_type='error')
            return pd.DataFrame()

    # expects a pandas data frame, containing a column with categories and a column with interpreted classification outputs
    # compares content from both columns and makes a summarizing statement about accuracy
    # returns accuracy in percent
    @staticmethod
    def evaluate_output(data_frame, col_name_categories=col_name_categories, col_name_outputs=col_name_result):
        classification_interpreter = SessionConfigReader.read_value(ClassificationInterpreter.classification_interpreter_key)
        if classification_interpreter == ClassificationInterpreter.classification_interpreter_custom1:
            return ClassificationInterpreterCustom1.evaluate_output(data_frame, col_name_categories=col_name_categories, col_name_outputs=col_name_outputs)
        elif classification_interpreter == ClassificationInterpreter.classification_interpreter_custom2:
            return ClassificationInterpreterCustom2.evaluate_output(data_frame, col_name_categories=col_name_categories, col_name_outputs=col_name_outputs)
        else:
            SessionLogger.log('Tried to evaluate classification. Specified ClassificationInterpreter is not supported.', log_type='error')
            return 0
