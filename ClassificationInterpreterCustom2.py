from Storage import Storage
from SessionLogger import SessionLogger
from CategoryListHandler import CategoryListHandler
from SessionConfigReader import SessionConfigReader
import numpy as np


class ClassificationInterpreterCustom2:

    col_name_categories = 'categories'
    new_col_name_cat_vec = 'category vector'
    col_name_class_out = 'classification output'
    col_name_result = 'result'
    ext_out_vecs = '_category_vectors'
    ext_categorized = '_categorized'
    threshold_key = 'classification_interpreter_output_threshold'

    # expects list of strings
    # returns a category vector, based on the stored category list
    @staticmethod
    def get_cat_vec(str_list):
        category_list = CategoryListHandler.read_categories()
        fv = np.zeros(len(category_list))
        idx = 0
        for cat in category_list:
            if cat in str_list:
                fv[idx] = 1
            idx = idx+1
        return fv

    # expects a pandas data frame, containing a category column
    # creates an output vector for training from each entry in the category column from the data frame and stores it in a new column
    # returns pandas data frame with added column for added output vectors
    @staticmethod
    def create_out_vectors(data_frame, col_name=col_name_categories, new_col_name=new_col_name_cat_vec, storage_level=0, storage_name=''):
        data_frame[new_col_name] = data_frame.apply(lambda x: ClassificationInterpreterCustom2.get_cat_vec(x[col_name]), axis=1)

        log_text = 'Category vectors for classifier training have been created (' + str(len(data_frame.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            storage_name = storage_name + ClassificationInterpreterCustom2.ext_out_vecs
            Storage.store_pd_frame(data_frame, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + new_col_name + '\').'
        SessionLogger.log(log_text)

        return data_frame

    # expects a classification output vector, a category list and an output threshold
    # returns a list with corresponding categories, based on the stored category list
    @staticmethod
    def get_categories_from_vec(vec, category_list, threshold):
        output_categories = list()
        idx = 0
        while idx < len(vec) and idx < len(category_list):
            if vec[idx] > threshold:
                output_categories.append(category_list[idx])
            idx = idx+1
        return output_categories

    # expects a pandas data frame, containing a column with classification output vectors
    # creates a list of categories from each classification output vector and stores it in a new column
    # returns pandas data frame with added column for added category lists
    @staticmethod
    def interpret_output(data_frame, col_name=col_name_class_out, new_col_name=col_name_result, storage_level=0, storage_name='', log=1):
        category_list = CategoryListHandler.read_categories()
        threshold = SessionConfigReader.read_value(ClassificationInterpreterCustom2.threshold_key)
        data_frame[new_col_name] = data_frame.apply(lambda x: ClassificationInterpreterCustom2.get_categories_from_vec(x[col_name], category_list, threshold), axis=1)

        log_text = 'Categories have been determined (' + str(len(data_frame.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            storage_name = storage_name + ClassificationInterpreterCustom2.ext_categorized
            Storage.store_pd_frame(data_frame, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)

        return data_frame

    # expects a pandas data frame, containing a column with categories and a column with interpreted classification outputs
    # compares content from both columns and makes a summarizing statement about accuracy
    # returns accuracy in percent
    @staticmethod
    def evaluate_output(data_frame, col_name_categories=col_name_categories, col_name_outputs=col_name_result):
        idx = 0
        matches = 0
        for index, row in data_frame.iterrows():
            categories = row[col_name_categories]
            if len(categories) > 0:
                category = categories[0]
            else:
                category = ''
            outputs = row[col_name_outputs]
            if len(outputs) > 0:
                output = outputs[0]
            else:
                output = ''
            if category == output and category != '':
                matches = matches+1
            idx = idx+1
        return matches/idx
