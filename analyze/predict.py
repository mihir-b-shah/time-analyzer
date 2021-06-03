
from abc import ABC, abstractmethod

class Predictor(ABC):
  @classmethod
  def make(cls, name):
    if(name == 'rand-forest'):
      return RandForestPredictor()
    elif(name == 'shallow-nn'):
      return ShallowNNPredictor() 

  @abstractmethod
  def name(self):
    return 'rand-forest'

  @abstractmethod
  def predict(self, vector):
    pass

  @abstractmethod
  def save(self, path):
    pass

class RandForestPredictor(Predictor):
  def name(self):
    return 'rand-forest'

  def predict(self, data):
    return False

  def save(self, path):
    pass

class ShallowNNPredictor(Predictor):
  def __init__(self):
    self.fv_buffer = []
   
  def name(self): 
    return 'shallow-nn'

  def predict(self, data):
    return False
  
  def save(self, path):
    pass
