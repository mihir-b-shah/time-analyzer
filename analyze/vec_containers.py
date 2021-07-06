
import vect_bytes

class VectorBag:

  @classmethod
  def read_helper(cls, fname):
    return vect_bytes.read_entries(read_entries(fname, [100, 300], 2))
    
  def __init__(self, fname, sampl_strat):
    arr = []
    with open(fname, 'rb'):
      entry = read_helper(fname)
      while(entry): 
        arr.append(entry)
        entry = read_helper(fname)
    self.stack = arr
    self.sampl_strat = sampl_strat

  # the only way uncertainty sampling can have linear cost.
  def sample(self, k, n):
    ret = []
    for i in range(len(self.stack), len(self.stack)-n, -1):
      if(self.sampl_strat.sample((len(ret), i, k, n), self.stack[-1])):
        ret.append(self.stack[-1])
      self.stack.pop() 
    return ret
