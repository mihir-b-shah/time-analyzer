
from abc import ABC, abstractmethod
import tensorflow.keras as keras
import utils
import d2v_model
import os
import sys

class Predictor(ABC):
  @classmethod
  def make(cls, name, eid):
    if(name == RandForestPredictor.name()):
      return RandForestPredictor(eid)
    elif(name == ShallowNNPredictor.name()):
      return ShallowNNPredictor(eid) 

  @abstractmethod
  def predict(self, vector):
    pass

  @abstractmethod
  def save(self, path):
    pass
  
class RandForestPredictor(Predictor):

  def __init__(self, eid):
    pass

  @classmethod
  def name(cls):
    return 'rand-forest'

  def predict(self, data):
    return False

  def save(self, path):
    pass

class ShallowNNPredictor(Predictor):
  def __init__(self, eid):
    self.eid = eid
    mpath = utils.get_path('models/users/%s/%s/model'%(self.eid, self.name()))
    if(os.path.exists(mpath)):
      self.model = keras.models.load_model(mpath)
    else:
      self.model = keras.Sequential()
      self.model.add(keras.Input(d2v_model.d2v_vect_length()))
      self.model.add(keras.layers.Dense(40, activation='relu'))
      self.model.add(keras.layers.Dense(1, activation='relu'))
   
  @classmethod
  def name(cls): 
    return 'shallow-nn'

  def predict(self, data):
    return False
  
  def save(self, path):
    self.model.save(path)
