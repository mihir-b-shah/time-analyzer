
import html_to_text
import preprocess
import extract
import predict

# one preprocessor, one extractor, one predictor
class Pipeline:
  def __init__(self, pre_name, extr_name, pred_name):
    self.pre = preprocess.Preprocessor.make(pre_name) 
    self.extr = extract.FeatureExtractor.make(extr_name)
    self.pred = predict.Predictor.make(pred_name)
    
  def predict(self, html):
    return self.pred.predict(self.extr.extract_fv(self.pre.preprocess(html_to_text.html_to_text(html))))
