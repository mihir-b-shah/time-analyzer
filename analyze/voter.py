
class Voter:
  def __init__(self, models, thr):
    self.models = models
    self.thr = thr
  
  def predict(self, data):
    ct = 0
    for model in self.models:
      ct += model.predict(data)
    return ct > self.thr*len(data)
