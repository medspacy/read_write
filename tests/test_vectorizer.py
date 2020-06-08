import unittest
from spacy.lang.en import English
from medspacy_io.reader import EhostDocReader
from medspacy_io.reader import EhostDirReader
from PyRuSH import PyRuSHSentencizer
from medspacy_io.vectorizer import Vectorizer


class TestEhostReader(unittest.TestCase):

    def setUp(self) -> None:
        self.nlp = English()
        self.nlp.add_pipe(PyRuSHSentencizer('conf/rush_rules.tsv'))

    def test_to_sents_df(self):
        ereader = EhostDocReader(nlp=self.nlp, schema_file='data/ehost_test_corpus/config/projectschema.xml',
                                 support_overlap=True)
        doc = ereader.read('data/ehost_test_corpus2/corpus/doc1.txt')
        print(len(list(doc.sents)))
        assert (len(doc._.concepts) == 3)
        assert (len(doc._.concepts['Nonspecific_SSTI']) == 1)
        df = Vectorizer.to_sents_df(doc)
        # print(df.shape)
        assert (df.shape[0] == 4)
        df = Vectorizer.to_sents_df(doc, sent_window=2)
        # print(df.shape)
        assert (df.shape[0] == 5)

    def test_to_sents_nparray(self):
        ereader = EhostDocReader(nlp=self.nlp, schema_file='data/ehost_test_corpus/config/projectschema.xml',
                                 support_overlap=True)
        doc = ereader.read('data/ehost_test_corpus2/corpus/doc1.txt')
        print(len(list(doc.sents)))
        assert (len(doc._.concepts) == 3)
        assert (len(doc._.concepts['Nonspecific_SSTI']) == 1)
        df = Vectorizer.to_sents_nparray(doc)
        print(df)
        assert (df.shape[0] == 4)
        df = Vectorizer.to_sents_nparray(doc, sent_window=2)
        print(df.shape)
        assert (df.shape[0] == 5)

    def test_docs_to_sents_df(self):
        dir_reader = EhostDirReader(txt_dir='data/ehost_test_corpus/',
                                    nlp=self.nlp, support_overlap=False,
                                    docReaderClass=EhostDocReader, recursive=True,
                                    schema_file='data/ehost_test_corpus/config/projectschema.xml')
        docs = dir_reader.read()
        df = Vectorizer.docs_to_sents_df(docs)
        assert (df.shape[0] == 12)
        df = Vectorizer.docs_to_sents_df(docs, sent_window=2)
        assert (df.shape[0] == 20)

    def test_docs_to_sents_df2(self):
        dir_reader = EhostDirReader(txt_dir='data/ehost_test_corpus2/',
                                    nlp=self.nlp, support_overlap=True,
                                    docReaderClass=EhostDocReader, recursive=True,
                                    schema_file='data/ehost_test_corpus/config/projectschema.xml')
        docs = dir_reader.read()
        df = Vectorizer.docs_to_sents_df(docs)
        assert (df.shape[0] == 12)
        df = Vectorizer.docs_to_sents_df(docs, sent_window=2)
        assert (df.shape[0] == 19)
