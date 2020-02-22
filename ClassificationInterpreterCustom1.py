from Vectorizer import Vectorizer
from Misc import Misc
from Storage import Storage
from SessionLogger import SessionLogger
from CategoryListHandler import CategoryListHandler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import numpy as np
from SessionConfigReader import SessionConfigReader


class ClassificationInterpreterCustom1:

    col_name_categories = 'categories'
    new_col_name_cat_vec = 'category vector'
    col_name_class_out = 'classification output'
    col_name_result = 'result'
    one_word_cat = 'one word category'
    ext_out_vecs = '_category_vectors'
    ext_categorized = '_categorized'
    similarity_function_key = 'similarity_function'
    sim_func_cosine = 'cosine_similarity'
    sim_func_eucl_dist = 'euclidean_distance'

    # expects list of strings
    # returns the first word from the first string element in the list
    @staticmethod
    def extract_one_word_cat(str_list):
        if len(str_list) == 0:
            return ''
        else:
            return Misc.extract_first_word(str_list[0])

    # expects a pandas data frame, containing a category column
    # creates an output vector for training from each entry in the category column from the data frame and stores it in a new column
    # returns pandas data frame with added column for added output vectors
    @staticmethod
    def create_out_vectors(data_frame, col_name=col_name_categories, new_col_name=new_col_name_cat_vec, storage_level=0, storage_name=''):
        df = data_frame.copy()
        df[ClassificationInterpreterCustom1.one_word_cat] = df.apply(lambda x: ClassificationInterpreterCustom1.extract_one_word_cat(x[col_name]), axis=1)
        vectorized_df = Vectorizer.vectorize(df, col_name=ClassificationInterpreterCustom1.one_word_cat, new_col_name=new_col_name, storage_level=0, log=0)
        vectorized_df = vectorized_df.drop(columns=[ClassificationInterpreterCustom1.one_word_cat])
        vectorized_df[new_col_name] = vectorized_df.apply(lambda x: (x[new_col_name]+1)/2, axis=1) # adjust to softmax codomain

        log_text = 'Category vectors for classifier training have been created (' + str(len(data_frame.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            storage_name = storage_name + ClassificationInterpreterCustom1.ext_out_vecs
            Storage.store_pd_frame(vectorized_df, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + new_col_name + '\').'
        SessionLogger.log(log_text)

        return vectorized_df

    # expects a vector and two lists with word strings and their vector representations
    # returns the word with the highest similarity in relation to the vector
    @staticmethod
    def get_highest_similarity(vec, word_list, word_vec_list):
        vec = vec*2-1 # adjust from softmax codomain
        sim_func = SessionConfigReader.read_value(ClassificationInterpreterCustom1.similarity_function_key)
        idx = 0
        sim = 0
        highest_word = ''
        for word in word_list:
            word_vec = word_vec_list[idx]
            new_sim = 0
            if word_vec is not None:
                if sim_func == ClassificationInterpreterCustom1.sim_func_cosine:
                    new_sim = cosine_similarity(np.asarray([word_vec]), [vec])[0][0]
                elif sim_func == ClassificationInterpreterCustom1.sim_func_eucl_dist:
                    new_sim = euclidean_distances([word_vec], [vec])[0][0]
                if new_sim < 0:
                    new_sim = new_sim*-1
            if new_sim > sim:
                sim = new_sim
                highest_word = word
            idx = idx+1
        return highest_word

    # expects a pandas data frame, containing a column with classification output vectors
    # creates a list of categories from each classification output vector and stores it in a new column
    # returns pandas data frame with added column for added category lists
    @staticmethod
    def interpret_output(data_frame, col_name=col_name_class_out, new_col_name=col_name_result, storage_level=0, storage_name='', log=1):
        df = data_frame.copy()
        category_list = CategoryListHandler.read_categories()
        category_vectors = Vectorizer.get_word_vectors(category_list)
        df[new_col_name] = df.apply(lambda x: [ClassificationInterpreterCustom1.get_highest_similarity(x[col_name], category_list, category_vectors)], axis=1)

        log_text = 'Categories have been determined (' + str(len(df.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            storage_name = storage_name + ClassificationInterpreterCustom1.ext_categorized
            Storage.store_pd_frame(df, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)

        return df

    # expects a pandas data frame, containing a column with categories and a column with interpreted classification outputs
    # compares content from both columns and makes a summarizing statement about accuracy
    # returns accuracy in percent
    @staticmethod
    def evaluate_output(data_frame, col_name_categories=col_name_categories, col_name_outputs=col_name_result):
        idx = 0
        matches = 0
        for index, row in data_frame.iterrows():
            category = ClassificationInterpreterCustom1.extract_one_word_cat(row[col_name_categories])
            output = row[col_name_outputs][0]
            if category == output:
                matches = matches+1
            idx = idx+1
        return matches/idx
