
from abc import ABC, abstractmethod
import d2v_model
import w2v_model
import functools
import utils
import numpy as np

'''
Note a much more efficient apporach:
run the pipeline up to this point in the browser.
w2v and d2v would have to be embedded in the browser.
then send the feature vector down.

'''

class FeatureExtractor(ABC):
  @classmethod
  def make(cls, name, pp):
    if(name == 'd2v'):
      return D2vExtractor(pp)
    elif(name == 'w2v-avg'):
      return W2vExtractor(pp) 

  def __init__(self, pp):
    self.pp = pp

  def extract_fv(self, bef_txt):
    utils.log('TXT', str(type(bef_txt)))
    txt = self.pp.preprocess(bef_txt)
    return self._extract_fv(txt)

  @abstractmethod
  def _extract_fv(self, text):
    pass

class D2vExtractor(FeatureExtractor):
  def __init__(self, pp):
    super().__init__(pp)
    self.mdl = d2v_model.get_d2v_model()  

  def _extract_fv(self, words):
    return self.mdl.infer_vector(words)

class W2vExtractor(FeatureExtractor):
  def __init__(self, pp):
    super().__init__(pp)
    self.mdl = w2v_model.get_w2v_model()

  def _extract_fv(self, words):
    if(len(words) == 0):
      return np.zeros((w2v_model.w2v_vect_length(),)) 
    else:
      return functools.reduce(lambda v1,v2 : v1+v2, map(lambda word : self.mdl[word], words))/len(words)
