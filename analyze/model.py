
from abc import ABC, abstractmethod
from preprocess import Preprocessor
from extract import FeatureExtractor
from predict import Predictor
import os
import utils
import vect_bytes
from actv_learn import LearnerSystem

class Model(ABC):

  @classmethod
  def build_model(cls, name):
    if(name == 'useless'):
      return UselessModel()
    else:
      return VotingModel()

  @abstractmethod
  def insert_and_decide(self, url, txt):
    pass

  @abstractmethod
  def list_to_label(self):
    pass

  @abstractmethod
  def process_labels(self, lbls):
    pass
  
  @abstractmethod
  def update_topics(self, topics):
    pass

  @abstractmethod
  def save(self, path):
    pass

class UselessModel(Model):

  def __init__(self):
    pass

  def insert_and_decide(self, url, txt):
    return False

  def list_to_label(self):
    return ['https://www.google.com', 'http://mudhaniu.x10host.com', 'https://stackoverflow.com']

  def process_labels(self, lbls):
    pass
  
  def update_topics(self, topics):
    pass
   
  def save(self, path):
    pass

class VotingModel(Model):

  '''
  Note the structure of models:
  
  models/
    users/
      <user-1>/
        unlabel_fv
        label_fv
        shallow-nn-model
        rand-forest-model
      ...
    <doc2vec-models>
    <word2vec-models>
  '''
  def __init__(self, eid):
    self.models = [
      Predictor.make('shallow-nn', eid, FeatureExtractor.make('d2v', Preprocessor.make('clean'))),
      Predictor.make('rand-forest', eid, FeatureExtractor.make('w2v-avg', Preprocessor.make('entity')))
    ]
    self.fvs = [None]*len(self.models)
    self.learner = LearnerSystem(eid, self.models)
  
  def insert_and_decide(self, url, txt):
    sm = 0
    for i,model in enumerate(self.models):
      fv, mpred = model.predict(txt[0])
      self.fvs[i] = fv
      sm += mpred

    self.learner.accept_unlabeled(url, self.fvs)
    return sm >= 0.5*len(self.models)

  def list_to_label(self):
    return self.learner.make_queries()

  def process_labels(self, lbls):
    self.learner.accept_labels(lbls)
  
  def update_topics(self, topics):
    pass

  def save(self, path):
    for model in self.models:
      model.save(os.path.join(path, '%s-model'%(model.name())))
