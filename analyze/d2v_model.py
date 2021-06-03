
from gensim.models.doc2vec import Doc2Vec
import utils

d2v = Doc2Vec.load(utils.get_path('models/d2v.model'))

def get_d2v_model():
  return d2v

