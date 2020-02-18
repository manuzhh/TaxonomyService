

class Misc:

    # expects pandas data frame and column name, representing text strings
    # returns list over list format of pandas data frame column
    @staticmethod
    def get_list_representation(data_frame, col_name):
        str_docs = data_frame[col_name].tolist()
        docs = list()
        for doc_string in str_docs:
            docs.append(doc_string.split())
        return docs

    # expects text string
    # returns first word from the string
    @staticmethod
    def extract_first_word(text: str):
        words = text.split()
        if len(words) > 0:
            return words[0]
        else:
            return ''
