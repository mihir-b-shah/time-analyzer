
from abc import ABC, abstractmethod
import tensorflow.keras as keras
import utils
import d2v_model
import os
import sys

class Predictor(ABC):
  @classmethod
  def make(cls, name):
    mpath = utils.get_path('models/unlabeled/%s/fv'%(name))
    if(name == RandForestPredictor.name()):
      if(os.path.exists(mpath)):
        return RandForestPredictor(mpath)
      else:
        return RandForestPredictor()
    elif(name == ShallowNNPredictor.name()):
      if(os.path.exists(mpath)):
        return ShallowNNPredictor(mpath) 
      else:
        return ShallowNNPredictor()

  @abstractmethod
  def predict(self, vector):
    pass

  @abstractmethod
  def save(self, path):
    pass
  
class RandForestPredictor(Predictor):

  def __init__(self, path=None):
    pass

  @classmethod
  def name(cls):
    return 'rand-forest'

  def predict(self, data):
    return False

  def save(self, path):
    pass

class ShallowNNPredictor(Predictor):
  def __init__(self, path=None, NumTopics=40):
    if(path == None):
      self.model = keras.Sequential()
      self.model.add(keras.Input(d2v_model.d2v_vect_length()))
      self.model.add(keras.layers.Dense(40, activation='relu'))
      self.model.add(keras.layers.Dense(1, activation='relu'))
    else:
      self.model = keras.models.load_model(path)
   
  @classmethod
  def name(cls): 
    return 'shallow-nn'

  def predict(self, data):
    return False
  
  def save(self, path):
    self.model.save(path)
