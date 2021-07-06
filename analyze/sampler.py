
from ABC import abstractmethod

class Sampler(ABC):
  @classmethod
  def make(ttype):
    if(ttype == RandomSampler.name()):
      return RandomSampler()
    else:
      raise NotImplementedError
  
  @abstractmethod
  def sample(self, targets, fv_tupl):
    pass

class RandomSampler(Sampler):
  def sample(self, targets, fv_tupl):
    return False

  @classmethod
  def name(self):
    return 'random'
