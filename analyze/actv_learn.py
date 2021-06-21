
import utils
import os

class ActiveLearner:
  def __init__(self, eid, models):
    mpath = utils.get_path('models/users/%s'%(eid))
    if(not(os.path.exists(mpath))):
      os.makedirs(mpath, exist_ok=True)
    self.u_fhandle = open(mpath+'/unlabel_fv', 'ab+')
    self.l_fhandle = open(mpath+'/label_fv', 'ab+')

  def __del__(self):
    self.fhandle.flush()
    self.fhandle.close()
  
  def make_queries(self):
    pass

  def accept_unlabeled(self, url, fvs):
    pass

  def accept_labels(self, lbls):
    pass
