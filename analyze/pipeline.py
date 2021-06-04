
import html_to_text
import preprocess
import extract
import predict
import utils

# one preprocessor, one extractor, one predictor
class Pipeline:
  def __init__(self, pre_name, extr_name, pred_name):
    self.pre = preprocess.Preprocessor.make(pre_name) 
    self.extr = extract.FeatureExtractor.make(extr_name)
    self.pred = predict.Predictor.make(pred_name)
    
  '''
  Note the structure of models:
  
  models/
    unlabeled/
      shallow-nn/
      rand-forest/
    users/
      <user-1>/
        shallow-nn/
        rand-forest/
      ...
    <doc2vec-models>
    <word2vec-models>
  '''
  def save_fv(self, fv):
    save_path = utils.get_path('models/unlabeled/%s/fv'%(self.pred.name()))

  def predict(self, html):
    fv = self.extr.extract_fv(self.pre.preprocess(html_to_text.html_to_text(html)))
    save_fv(fv)
    return self.pred.predict(fv)
