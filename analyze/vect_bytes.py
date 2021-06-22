
import numpy as np

'''
Utilities to read and write numpy vectors of to my memory file
'''

def write_entries(fhandle, tupl):
  url, vs = tupl
  fhandle.write(bytes([len(url)]))
  fhandle.write(bytes(url, encoding='utf8'))
  for i in range(len(vs)):
    fhandle.write(vs[i].tobytes())

# size is either 100 or 300 of vectors
def read_entries(fhandle, sizes, n):
  url_len_bytes = fhandle.read(1)
  if(not(url_len_bytes)):
    return None

  url_len = int.from_bytes(url_len_bytes, byteorder='little')
  url = fhandle.read(url_len)

  vs = [None]*n
  for i in range(n):
    vs[i] = np.ndarray((sizes[i],), np.float32, fhandle.read(sizes[i]*4))

  return (url, vs)
