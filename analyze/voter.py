
import os

class Voter:
  def __init__(self, models, thr):
    self.models = models
  
  def predict(self, data):
    ct = 0
    for model in self.models:
      ct += model.predict(data)
    return ct > thr*len(data)

  def save(self, path):
    for model in self.models:
      model.save(os.path.join(path, model.name()))
