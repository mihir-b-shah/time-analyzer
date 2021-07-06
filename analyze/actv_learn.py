
import utils
import os
import vec_containers
from sampler import Sampler

class LearnerSystem:
  def __init__(self, eid, models):
    self.models = models
    mpath = utils.get_path('models/users/%s'%(eid))
    if(not(os.path.exists(mpath))):
      os.makedirs(mpath, exist_ok=True)
    u_bag = vec_containers.VectorBag(mpath+'/unlabel_fv', Sampler.make('random'))

  def __del__(self):
    pass
  
  '''
  1. Learner (has VectorBag as an instance variable - which represents the (url, fv...) tuples in a stack
  2. Sampler (a method on the learner that pops from the stack and gives certain samples for decision)
  3. Active Learner (for each model, decide whether useful)
  4. Voter (combine the useful/not-useful decisions) on whether to request the sample
  '''
  def make_queries(self, thr):
    return list(filter(lambda take: 
                sum(map(lambda i,fv:self.models[i].want_label(fv), 
                enumerate(samples)))/len(self.models) >= thr, samples))
