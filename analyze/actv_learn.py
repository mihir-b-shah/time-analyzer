
import utils
import os
import vec_containers

'''
idea is, do active learning on the first vector set and use
the second to verify against first
'''

class ActiveLearner:
  def __init__(self, eid, models):
    mpath = utils.get_path('models/users/%s'%(eid))
    if(not(os.path.exists(mpath))):
      os.makedirs(mpath, exist_ok=True)
    u_bag = vec_containers.VectorBag(mpath+'/unlabel_fv')

  def __del__(self):
    self.fhandle.flush()
    self.fhandle.close()
  
  '''
  1. Learner (has VectorBag as an instance variable - which represents the (url, fv...) tuples in a stack
  2. Sampler (a method on the learner that pops from the stack and gives certain samples for decision)
  3. Active Learner (for each model, decide whether useful)
  4. Voter (combine the useful/not-useful decisions) on whether to request the sample
  '''
  def make_queries(self):
    pass

  def accept_unlabeled(self, url, fvs):
    pass

  def accept_labels(self, lbls):
    pass
