from gensim.models import Word2Vec
from Storage import Storage
from SessionConfigReader import SessionConfigReader
from WordVecToDocVec import WordVecToDocVec
from Misc import Misc
from SessionLogger import SessionLogger


class VectorizerGensimWord2Vec:

    model_id_key = 'vec_model_id'
    dimension_key = 'word2vec_size'
    window_size_key = 'word2vec_window'
    min_count_key = 'word2vec_min_count'
    n_workers_key = 'word2vec_workers'
    col_name = 'preprocessed'
    new_col_name = 'document vector'
    ext_vectorized = '_vectorized'
    class_out_col_name = 'classification output'

    # returns the model identifier, specified in the session config
    @staticmethod
    def get_model_id():
        return SessionConfigReader.read_value(VectorizerGensimWord2Vec.model_id_key)

    # expects string list of words and a model
    # creates word vectors for each word in text, if word is not contained in the model's dictionary the vector is None
    # returns list of word vectors
    @staticmethod
    def get_word_vectors_m(words, model):
        word_vectors = list()
        for word in words:
            if word in model.wv.vocab:
                word_vectors.append(model[word])
            else:
                word_vectors.append(None)
        return word_vectors

    # expects string list of words, optionally a model id
    # creates word vectors for each word in text, if word is not contained in the model's dictionary the vector is None
    # returns list of word vectors
    @staticmethod
    def get_word_vectors(words, model_id=''):
        if model_id == '':
            model_id = VectorizerGensimWord2Vec.get_model_id()
        model = Storage.load_model(model_id)
        return VectorizerGensimWord2Vec.get_word_vectors_m(words, model)

    # expects a text string the model id
    # vectorizes the string, using Word Embedding To Doc Embedding Algorithm specified in the session config
    # returns vectorized string
    @staticmethod
    def process_text(text: str, model):
        word_vectors = VectorizerGensimWord2Vec.get_word_vectors_m(text.split(), model)
        doc_vector = WordVecToDocVec.get_doc_vec(word_vectors)
        return doc_vector

    # expects pandas data frame, optionally an identifier for the new model and a column name from which the model should be created
    # creates a word embedding model with the texts from the the data frame and trains the model
    # returns the identifier of the new model
    @staticmethod
    def create_model(data_frame, new_model_id=None, col_name=col_name):
        config_keys = list()
        config_keys.append(VectorizerGensimWord2Vec.model_id_key)
        config_keys.append(VectorizerGensimWord2Vec.dimension_key)
        config_keys.append(VectorizerGensimWord2Vec.window_size_key)
        config_keys.append(VectorizerGensimWord2Vec.min_count_key)
        config_keys.append(VectorizerGensimWord2Vec.n_workers_key)
        config = SessionConfigReader.read_values(config_keys)
        model_id = config[0]
        dimension = config[1]
        window_size = config[2]
        min_count = config[3]
        n_workers = config[4]
        docs = Misc.get_list_representation(data_frame, col_name)
        model = Word2Vec(docs, size=dimension, window=window_size, min_count=min_count, workers=n_workers)
        if new_model_id is None:
            new_model_id = model_id
        Storage.store_model(model, new_model_id)
        SessionLogger.log('Created new gensim word2vec model. Stored in \'' + new_model_id + '\'.')
        return new_model_id

    # expects pandas data frame, optionally an identifier for the model to train and a column name referencing the new texts in the pandas data frame
    # returns the model identifier
    @staticmethod
    def train_model(data_frame, model_id=None, col_name=col_name):
        if model_id is None:
            model_id = VectorizerGensimWord2Vec.get_model_id()
        model = Storage.load_model(model_id)
        docs = Misc.get_list_representation(data_frame, col_name)
        model.train(docs, total_examples=1, epochs=1)
        Storage.store_model(model, model_id)
        SessionLogger.log('Trained gensim word2vec model \'' + model_id + '\' with ' + str(len(data_frame.index)) + ' new texts.')
        return model_id

    # expects pandas data frame, optionally an identifier for the model to use for vectorization and a column name referencing texts in the pandas data frame to vectorize
    # vectorizes the texts from the data frame with the specified model and optionally stores the vectorized texts in a new pandas data frame in the storage system
    # returns vectorized pandas data frame
    @staticmethod
    def vectorize(data_frame, model_id=None, col_name=col_name, new_col_name=new_col_name, storage_level=0, storage_name='', log=1):
        if model_id is None:
            model_id = VectorizerGensimWord2Vec.get_model_id()
        model = Storage.load_model(model_id)
        data_frame[new_col_name] = data_frame.apply(lambda x: VectorizerGensimWord2Vec.process_text(x[col_name], model), axis=1)
        log_text = 'Vectorized documents (' + str(len(data_frame.index)) + ' entries).'
        if storage_level >= 1 and storage_name != '':
            storage_name = storage_name + VectorizerGensimWord2Vec.ext_vectorized
            Storage.store_pd_frame(data_frame, storage_name)
            log_text = log_text + ' Stored in \'' + storage_name + '\' (column: \'' + new_col_name + '\').'
        if log:
            SessionLogger.log(log_text)
        return data_frame
