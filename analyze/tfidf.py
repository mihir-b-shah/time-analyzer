
from sklearn.feature_extraction.text import TfidfVectorizer
from iterate_docs import DocIterator
from array import *
import collections as colc
import math

# simpler not to subclass
class GrowableSparseMatrix:
    def __init__(self, none_val = None):
        self.mat = list(dict())
        self.NoneVal = none_val

    def add_row(self, k):
        for i in range(k):
            self.mat.append(dict())

    def __getitem__(self, index):
        i,j = index
        this_dict = self.mat[i]
        return this_dict[j] if j in this_dict else self.NoneVal

    def __setitem__(self, index, v):
        i,j = index
        self.mat[i][j] = v

    def get_row(self, i):
        return self.mat[i]

    def __len__(self):
        return len(self.mat)

class StreamTFIDF:
    def __init__(self):
        self.term_map = dict()
        self.tdm = GrowableSparseMatrix(0)
        self.idv = array('I') # unsigned array

    def _tokenize(self, doc):
        return doc.split(' ')

    def _new_word(self, word):
        size = len(self.term_map)
        self.term_map[word] = size

        # setup for idf
        self.idv.append(0)

        return size

    def _normalize(self, row, doc_len):
        for k in row:
            row[k] /= doc_len

    def add_docs(self, docs):
        doc_alias = len(self.tdm)

        self.tdm.add_row(len(docs))
        for doc in docs:
            word_list = self._tokenize(doc)
            num_words = len(word_list)
            toks = colc.Counter(word_list)

            for (tok, count) in toks.items():
                tok_alias = self.term_map[tok] if (tok in self.term_map) else self._new_word(tok)

                # update tf
                self.tdm[doc_alias, tok_alias] = count

                # update idf
                self.idv[tok_alias] += 1
            
            # normalize term frequencies.
            self._normalize(self.tdm.get_row(doc_alias), num_words)

            doc_alias += 1

    # term is a word, doc is an alias
    def score(self, term, doc):
        term_alias = self.term_map[term]
        return self.tdm[doc, term_alias]*math.log(len(self.tdm)/self.idv[term_alias])

# returns a sparse matrix.
def get_tf():
    docs = [doc for doc in DocIterator()]
    cv = TfidfVectorizer()
    return cv.fit_transform(docs)

docs = [doc for doc in DocIterator()]
st = StreamTFIDF()
for doc in docs:
    st.add_docs([doc])