
import html_to_text
import preprocess
import extract
import predict
import utils
import os

# one preprocessor, one extractor, one predictor
class Pipeline:
  def __init__(self, pre, extr, pred, eid):
    self.pre = pre 
    self.extr = extr
    self.pred = pred

    mpath = utils.get_path(('models/users/%s/'%(eid))+self.pred.name())
    if(not(os.path.exists(mpath))):
      os.makedirs(mpath, exist_ok=True)
    self.fhandle = open(mpath+'/unlabel_fv', 'ab')
    
  def __del__(self):
    self.fhandle.flush()
    self.fhandle.close()

  '''
  Note the structure of models:
  
  models/
    users/
      <user-1>/
        shallow-nn/
          unlabeled/
          labeled/
        rand-forest/
          unlabeled/
          labeled/
      ...
    <doc2vec-models>
    <word2vec-models>
  '''
  def save_fv(self, fv):
    for i in range(len(fv)):
      self.fhandle.write(fv[i].tobytes())

  def predict(self, text):
    fv = self.extr.extract_fv(self.pre.preprocess(text[0]))
    self.save_fv(fv)
    return self.pred.predict(fv)

  def save(self, path):
    self.pred.save(path)

  def name(self):
    return self.pred.name()
