
from abc import ABC, abstractmethod
import d2v_model
import w2v_model

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

  def extract_fv(words):
    return self.mdl.infer_vector(words)

class W2vExtractor(FeatureExtractor):
  def __init__(self):
    self.mdl = w2v_model.get_w2v_model()

  def extract_fv(words):
    return reduce(lambda v1,v2 : v1+v2, map(lambda word : self.mdl[word], words))/len(words)
