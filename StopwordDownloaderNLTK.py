import nltk
from nltk.corpus import stopwords
from StopwordHandler import StopwordHandler
from SessionLogger import SessionLogger


class StopwordDownloaderNLTK:

    german = 'german'

    # downloads and optionally stores stopwords from NLTK
    # returns set with NLTK stopwords
    @staticmethod
    def get_stopwords(language=german, store=1, log=1):
        nltk.download('stopwords')
        sw = set(stopwords.words(language))
        log_text = str(len(sw)) + ' stop words downloaded from NLTK.'
        if log:
            SessionLogger.log(log_text)
        if store:
            StopwordHandler.set_stopwords(sw)
        return sw
