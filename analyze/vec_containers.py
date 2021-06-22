
import vect_bytes

class VectorBag:

  @classmethod
  def read_helper(cls, fname):
    return vect_bytes.read_entries(read_entries(fname, [100, 300], 2))
    
  @classmethod
  def build(cls, fname):
    arr = []
    with open(fname, 'rb'):
      entry = read_helper(fname)
      while(entry): 
        arr.append(entry)
        entry = read_helper(fname)
    return VectorBag(arr)

  def __init__(self, stack):
    self.stack = stack
