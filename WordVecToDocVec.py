from WordVecToDocVecCustom import WordVecToDocVecCustom
from SessionConfigReader import SessionConfigReader


class WordVecToDocVec:

    word_vec_to_doc_vec_key = 'word-vec_to_doc-vec'
    word_vec_to_doc_vec_custom = 'custom'

    # expects a list of word vectors
    # creates a document vector from word vectors
    # returns the document vector
    @staticmethod
    def get_doc_vec(word_vectors):
        word_emb_to_doc_emb_type = SessionConfigReader.read_value(WordVecToDocVec.word_vec_to_doc_vec_key)
        if word_emb_to_doc_emb_type == WordVecToDocVec.word_vec_to_doc_vec_custom:
            return WordVecToDocVecCustom.get_doc_vec(word_vectors)
