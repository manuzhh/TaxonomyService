from SessionLogger import SessionLogger
from SessionConfigReader import SessionConfigReader
from TenKGnadImporter import TenKGnadImporter


class CorpusImporter:

    corpus_importer_key = 'corpus_importer'
    tenkgnad_importer = 'TenKGNAD'

    # stores content from corpus in a pandas data frame in the storage system
    # returns identifier of pandas data frame in storage system, with data frame containing a column 'category' and a column 'text'
    @staticmethod
    def import_docs():
        importer_type = SessionConfigReader.read_value(CorpusImporter.corpus_importer_key)
        if importer_type == CorpusImporter.tenkgnad_importer:
            return TenKGnadImporter.import_docs()
        else:
            SessionLogger.log('Tried to import corpus. Specified Corpus Importer is not supported.', log_type='error')
            return ''
