
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
import utils

def w2v_vect_length():
  return 300

w2v_model = KeyedVectors.load(get_tmpfile(utils.get_path('models/vectors.kv')), mmap='r')

def in_corpus(word):
  return word in w2v_model.vocab

def get_w2v_model():
  return w2v_model
