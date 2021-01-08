
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors

def get_w2v_model():
    filename = get_tmpfile("../../../data/vectors.kv")
    return KeyedVectors.load(filename, mmap='r')

print(get_w2v_model()['cat'].shape)
