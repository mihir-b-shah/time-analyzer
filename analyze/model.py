
from abc import ABC, abstractmethod
from voter import Voter
from preprocess import Preprocessor
from extract import FeatureExtractor
from predict import Predictor
from pipeline import Pipeline
import os

class Model(ABC):

  @classmethod
  def build_model(cls, name):
    if(name == 'useless'):
      return UselessModel()
    else:
      return VotingModel()

  @abstractmethod
  def insert_and_decide(self, email, txt):
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

  def insert_and_decide(self, email, txt):
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

  def __init__(self, Threshold=0.5):
    self.models = [
      Pipeline(Preprocessor.make('clean'), FeatureExtractor.make('d2v'), Predictor.make('shallow-nn')),
      Pipeline(Preprocessor.make('entity'), FeatureExtractor.make('w2v-avg'), Predictor.make('rand-forest'))
    ]
    self.voter = Voter(self.models, Threshold)

  def insert_and_decide(self, email, txt):
    ret = self.voter.predict(txt)
    
  def list_to_label(self):
    return []

  def process_labels(self, lbls):
    pass
  
  def update_topics(self, topics):
    pass

  def save(self, path):
    for model in self.models:
      model.save(os.path.join(path, model.name()))
