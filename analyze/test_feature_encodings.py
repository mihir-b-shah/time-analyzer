
import csv
import iterate_docs
import tfidf
import lda
import gensim_model
import numpy as np
import timeit

def _get_test_set(fname):
    with open('../../../data/test/%s.csv'%(fname), 'r') as csvfile:
        reader = csv.reader(csvfile)
        return [row for row in reader]

def _build_tfidf_model(docs):
    model = tfidf.TFIDFStreamer()
    model.add_docs(docs)
    return model

_K_Tfidf = 5
def _tfidf_w2v(doc_alias, w2v_model, tf_idf_model):
    return tf_idf_model.get_vector(_K_Tfidf, doc_alias, w2v_model)

_NumTopics = 300
def _build_lda_model(docs):
    return lda.update_full_and_extract(lda.build_model(_NumTopics), docs)

def _lda(doc_alias, model):
    return model[doc_alias]

def _build_d2v():
    return gensim_model.get_d2v_model()

def _get_d2v_vector(doc_alias, docs, model):
    return model.infer_vector(docs[doc_alias].split(' '))

def normalized_dot(v1, v2):
    return np.dot(v1, v2)/np.sqrt(np.linalg.norm(v1)*np.linalg.norm(v2))

def run_test(s,e):
    docs = iterate_docs.get_docs()[s:e]

    tfidf_model = _build_tfidf_model(docs)
    lda_model = _build_lda_model(docs)
    d2v_model = _build_d2v()
    gensim_w2v_model = gensim_model.get_w2v_model()

    tests = _get_test_set('test_data')
    tests = list(map(lambda tupl : (int(tupl[0]), int(tupl[1]), int(tupl[2])), tests))

    ct = 0
    tfidf_mse = 0
    lda_mse = 0
    d2v_mse = 0

    for (doc_alias_1, doc_alias_2, score) in tests:
        if(score == 0):
            continue

        score = score/50 - 1

        tfidf_mse = (score - normalized_dot(_tfidf_w2v(doc_alias_1, gensim_w2v_model, tfidf_model), 
                        _tfidf_w2v(doc_alias_2, gensim_w2v_model, tfidf_model)))**2

        lda_mse = (score - normalized_dot(_lda(doc_alias_1, lda_model), 
                        _lda(doc_alias_2, lda_model)))**2

        d2v_mse = (score - normalized_dot(_get_d2v_vector(doc_alias_1, docs, d2v_model), 
                        _get_d2v_vector(doc_alias_2, docs, d2v_model)))**2

        ct += 1

    tfidf_mse /= ct
    lda_mse /= ct
    d2v_mse /= ct

    print('TF-IDF mean squared error: ' + str(tfidf_mse))
    print('LDA mean squared error: ' + str(lda_mse))
    print('Doc2Vec mean squared error: ' + str(d2v_mse))

print('Time taken: ' + str(timeit.timeit(lambda: run_test(0,500), number=1)))