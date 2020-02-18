import numpy as np
from SessionConfigReader import SessionConfigReader


class WordVecToDocVecCustom:

    dimension_key = 'feature_vec_dim'

    # expects a list of word vectors
    # creates a document vector from word vectors (average of all word vectors)
    # returns the document vector
    @staticmethod
    def get_doc_vec(word_vectors):
        n_words = SessionConfigReader.read_value(WordVecToDocVecCustom.dimension_key)
        fv = np.zeros(n_words)
        idx = 0
        err = 0
        for vec in word_vectors:
            if vec is None:
                err = err+1
            else:
                fv = fv + vec
            idx = idx+1
            if idx == n_words:
                break
        return fv/(idx+1-err)
