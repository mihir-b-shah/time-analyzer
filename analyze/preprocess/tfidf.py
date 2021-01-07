
from sklearn.feature_extraction.text import CountVectorizer
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
        self.idv = array()

    def _tokenize(doc):
        return doc.split(' ')

    def _new_word(word):
        size = len(term_map)
        term_map[word] = size

        # setup for idf
        idv.append(0)

        return size

    def _normalize(row, doc_len):
        for k in d:
            d[k] /= doc_len

    def add_docs(self, docs):
        doc_alias = len(self.dtm)

        self.tdm.add_row(len(docs))
        for doc in docs:
            word_list = _tokenize(doc)
            num_words = len(word_list)
            toks = colc.Counter(word_list)

            for (tok, count) in toks:
                tok_alias = self.term_map[tok] if (tok in self.term_map) else _new_word(tok)

                # update tf
                self.tdm[doc_alias, tok_alias] = count

                # update idf
                self.idv[tok_alias] += 1
            
            # normalize term frequencies.
            _normalize(get_row(doc_alias), num_words)

            doc_alias += 1

    # term is a word, doc is an alias
    def score(self, term, doc):
        term_alias = self.term_map[term]
        return self.tdm[doc, term_alias]*math.log(len(self.tdm)/self.idv[term_alias])

# returns a sparse matrix.
def get_tf():
    docs = [doc for doc in DocIterator()]
    cv = CountVectorizer()
    return cv.fit_transform(docs)