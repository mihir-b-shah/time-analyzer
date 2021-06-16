
import numpy as np

'''
Utilities to read and write numpy vectors of to my memory file
'''

def write_entry(fhandle, tupl):
  url, vs = tupl
  fhandle.write(bytes(len(url)))
  fhandle.write(bytes(url, encoding='utf8'))
  for i in range(len(vs)):
    fhandle.write(vs[i].tobytes())

# size is either 100 or 300 of vectors
def read_entry(fhandle, size, n):
  url_len = fhandle.read(1)
  url = fhandle.read(url_len)

  vs = [None]*n
  for i in range(n):
    vs[i] = np.ndarray((size,), np.float32, fhandle.read(size*4))

  return (url, vs)
