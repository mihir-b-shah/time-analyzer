
import html_to_text
import preprocess
import extract
import predict
import utils
import os

# one preprocessor, one extractor, one predictor
class Pipeline:
  def __init__(self, pre, extr, pred):
    self.pre = pre 
    self.extr = extr
    self.pred = pred

    mpath = utils.get_path('models/unlabeled/'+self.pred.name())
    if(not(os.path.exists(mpath))):
      os.makedirs(mpath, exist_ok=True)
    self.fhandle = open(mpath+'fv', 'ab')
    
  def __del__(self):
    self.fhandle.flush()
    self.fhandle.close()

  '''
  Note the structure of models:
  
  models/
    unlabeled/
      shallow-nn/
        fv
      rand-forest/
        fv
    users/
      <user-1>/
        shallow-nn/
        rand-forest/
      ...
    <doc2vec-models>
    <word2vec-models>
  '''
  def save_fv(self, fv):
    for i in range(len(fv)):
      self.fhandle.write(fv[i].tobytes())

  def predict(self, text):
    utils.log('TEXT', str(text[0]))
    utils.log('PP_TYPE', str(type(self.pre)))
    utils.log('PP_RES', str(self.pre.preprocess(text[0])))
    fv = self.extr.extract_fv(self.pre.preprocess(text[0]))
    self.save_fv(fv)
    return self.pred.predict(fv)

  def save(self, path):
    self.pred.save(path)
