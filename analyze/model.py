
from abc import ABC, abstractmethod
import voter
import preprocess
import extract
import predict

class Model(ABC):

  @classmethod
  def build_model(cls, name):
    if(name == 'useless'):
      return UselessModel()

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

  def __init__(self):
    self.model = voter.Voter(Pipeline(preprocess.make('clean'), extract.make('d2v'), predict.make('shallow-nn')),
                             Pipeline(preprocess.make('entity'), extract.make('w2v-avg'), predict.make('rand-forest')),
                             0.5)

  def insert_and_decide(self, email, txt):
    ret = self.model.predict(txt)
    

  def list_to_label(self):
    return []

  def process_labels(self, lbls):
    pass
  
  def update_topics(self, topics):
    pass

  def save(self, path):
    self.model.save(path)
