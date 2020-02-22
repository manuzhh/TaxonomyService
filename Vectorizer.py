import pandas as pd
from VectorizerGensimWord2Vec import VectorizerGensimWord2Vec
from SessionConfigReader import SessionConfigReader
from SessionLogger import SessionLogger


class Vectorizer:

    model_id_key = 'vec_model_id'
    col_name = 'preprocessed'
    new_col_name = 'document vector'
    vectorizer_key = 'vectorizer'
    vectorizer_gensim_w2v = 'gensim-word2vec'

    # returns the model identifier, specified in the session config
    @staticmethod
    def get_model_id():
        return SessionConfigReader.read_value(Vectorizer.model_id_key)

    # expects string list of words, optionally a model id
    # creates word vectors for each word in text, if word is not contained in the model's dictionary the vector is None
    # returns list of word vectors
    @staticmethod
    def get_word_vectors(words, model_id=''):
        vectorizer_type = SessionConfigReader.read_value(Vectorizer.vectorizer_key)
        if vectorizer_type == Vectorizer.vectorizer_gensim_w2v:
            return VectorizerGensimWord2Vec.get_word_vectors(words, model_id=model_id)
        else:
            return list()

    # expects pandas data frame, optionally an identifier for the new model and a column name from which the model should be created
    # creates a word vector model with the texts from the the data frame and trains the model
    # returns the identifier of the new model
    @staticmethod
    def create_model(data_frame, new_model_id=None, col_name=col_name):
        vectorizer_type = SessionConfigReader.read_value(Vectorizer.vectorizer_key)
        if vectorizer_type == Vectorizer.vectorizer_gensim_w2v:
            return VectorizerGensimWord2Vec.create_model(data_frame, new_model_id=new_model_id, col_name=col_name)
        else:
            SessionLogger.log('Tried to create vector model. Specified Vectorizer is not supported.', log_type='error')
            return ''

    # expects pandas data frame, optionally an identifier for the model to train and a column name referencing the new texts in the pandas data frame
    # returns the model identifier
    @staticmethod
    def train_model(data_frame, model_id=None, col_name=col_name):
        vectorizer_type = SessionConfigReader.read_value(Vectorizer.vectorizer_key)
        if vectorizer_type == Vectorizer.vectorizer_gensim_w2v:
            return VectorizerGensimWord2Vec.train_model(data_frame, model_id=model_id, col_name=col_name)
        else:
            SessionLogger.log('Tried to train vector model. Specified Vectorizer is not supported.', log_type='error')
            return ''

    # expects pandas data frame, optionally an identifier for the model to use for vectorization and a column name referencing texts in the pandas data frame to vectorize
    # vectorizes the texts from the data frame with the specified model and optionally stores the vectorized texts in a new pandas data frame in the storage system
    # returns vectorized pandas data frame
    @staticmethod
    def vectorize(data_frame, model_id=None, col_name=col_name, new_col_name=new_col_name, storage_level=0, storage_name='', log=1):
        vectorizer_type = SessionConfigReader.read_value(Vectorizer.vectorizer_key)
        if vectorizer_type == Vectorizer.vectorizer_gensim_w2v:
            return VectorizerGensimWord2Vec.vectorize(data_frame, model_id, col_name, new_col_name, storage_level=storage_level, storage_name=storage_name, log=log)
        else:
            if log:
                SessionLogger.log('Tried to vectorize texts. Specified Vectorizer is not supported.', log_type='error')
            return pd.DataFrame()
