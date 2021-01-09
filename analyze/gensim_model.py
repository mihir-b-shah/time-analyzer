
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec

def w2v_vect_length():
    return 300

def get_w2v_model():
    filename = get_tmpfile("../../../data/vectors.kv")
    return KeyedVectors.load(filename, mmap='r')

def get_d2v_model():
    return Doc2Vec.load("../../../data/d2v.model")

get_d2v_model()