
from abc import ABC, abstractmethod
import d2v_model
import w2v_model
import functools
import utils

'''
Note a much more efficient apporach:
run the pipeline up to this point in the browser.
w2v and d2v would have to be embedded in the browser.
then send the feature vector down.

'''

class FeatureExtractor(ABC):
  @classmethod
  def make(cls, name):
    if(name == 'd2v'):
      return D2vExtractor()
    elif(name == 'w2v-avg'):
      return W2vExtractor() 

  @abstractmethod
  def extract_fv(self, text):
    pass

class D2vExtractor(FeatureExtractor):
  def __init__(self):
    self.mdl = d2v_model.get_d2v_model()  

  def extract_fv(self, words):
    return self.mdl.infer_vector(words)

class W2vExtractor(FeatureExtractor):
  def __init__(self):
    self.mdl = w2v_model.get_w2v_model()

  def extract_fv(self, words):
    return functools.reduce(lambda v1,v2 : v1+v2, map(lambda word : self.mdl[word], words))/len(words)