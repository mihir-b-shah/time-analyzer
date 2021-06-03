
from abc import ABC, abstractmethod

class Predictor(ABC):
  @classmethod
  def make(cls, name):
    if(name == 'rand-forest'):
      return RandForestPredictor()
    elif(name == 'shallow-nn'):
      return ShallowNNPredictor() 

  @abstractmethod
  def predict(self, vector):
    pass

class RandForestPredictor(Predictor):
  def predict(data):
    return False
    pass

class ShallowNNPredictor(Predictor):
  def __init__(self):
    self.fv_buffer = []
    

  def predict(data):
    return False
