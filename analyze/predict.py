
from abc import ABC, abstractmethod
import tensorflow.keras as keras
import utils
import d2v_model

class Predictor(ABC):
  @classmethod
  def make(cls, name):
    if(name == RandForestPredictor.name()):
      return RandForestPredictor()
    elif(name == ShallowNNPredictor.name()):
      return ShallowNNPredictor() 

  @abstractmethod
  def predict(self, vector):
    pass

  @abstractmethod
  def save(self, path):
    pass

class RandForestPredictor(Predictor):
  @classmethod
  def name(cls):
    return 'rand-forest'

  def predict(self, data):
    return False

  def save(self, path):
    pass

class ShallowNNPredictor(Predictor):
  def __init__(self, NumTopics=40, BatchSize=32):
    self.fv_buffer = [None]*BatchSize
    self.buf_ptr = 0

    self.model = keras.model.Sequential()
    self.model.add(keras.Input(d2v_model.d2v_vect_length()))
    self.model.add(keras.layers.Dense(40, activation='relu'))
    self.model.add(keras.layers.Dense(1, activation='relu'))
   
  @classmethod
  def name(cls): 
    return 'shallow-nn'

  def predict(self, data):
    if(buf_ptr < len(fv_buffer)):
      # train on the buffer feature_vector
    return False
  
  def save(self, path):
    self.model.save(path)
