
from sklearn.feature_extraction.text import TfidfVectorizer
from iterate_docs import DocIterator
from array import *
import collections as colc
import math
from functools import cmp_to_key

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

class TFIDFStreamer:
    def __init__(self):
        self.term_map = dict()
        self.rev_term_map = []
        self.tdm = GrowableSparseMatrix(0)
        self.idv = array('I') # unsigned array

    def _tokenize(self, doc):
        return doc.split(' ')

    def _new_word(self, word):
        size = len(self.term_map)
        self.term_map[word] = size
        self.rev_term_map.append(word)

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
                if(len(tok) < 3):
                    continue

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

    def get_most_freq(self, doc, k, skip=0, Insert=False):
        doc_alias = None
        if(Insert):
            add_docs([doc])
            doc_alias = len(self.dtm)-1
        else:
            doc_alias = doc

        row_cts = self.tdm.get_row(doc_alias)
        words = [(word := self.rev_term_map[idx], self.score(word, doc_alias)) for (idx, tf) in row_cts.items()]

        # sort in reverse order
        words = sorted(words, key=cmp_to_key(lambda p1,p2 : p2[1]-p1[1]))
        return words[skip: k+skip]
