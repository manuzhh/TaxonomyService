import pandas as pd
from TextPreprocessor import TextPreprocessor
from Vectorizer import Vectorizer
from Classifier import Classifier
from ClassificationInterpreter import ClassificationInterpreter


class Categorizer:

    text_col_name = 'text'
    prep_col_name = 'preprocessed'
    vec_col_name = 'vectorized'
    classified_col_name = 'classified'
    result_col_name = 'result'

    # expects list of text strings
    # returns list of lists of category strings
    @staticmethod
    def categorize_texts(texts):
        data_frame = pd.DataFrame(texts, columns=[Categorizer.text_col_name])
        data_frame = TextPreprocessor.preprocess_texts(data_frame, col_name=Categorizer.text_col_name, new_col_name=Categorizer.prep_col_name, storage_level=0, storage_name='', log=1)
        data_frame = Vectorizer.vectorize(data_frame, col_name=Categorizer.prep_col_name, new_col_name=Categorizer.vec_col_name, storage_level=0, storage_name='', log=1)
        data_frame = Classifier.classify(data_frame, col_name=Categorizer.vec_col_name, new_col_name=Categorizer.classified_col_name, storage_level=0, storage_name='', log=1)
        data_frame = ClassificationInterpreter.interpret_output(data_frame, col_name=Categorizer.classified_col_name, new_col_name=Categorizer.result_col_name, storage_level=0, storage_name='', log=1)
        return data_frame[Categorizer.result_col_name].tolist()
