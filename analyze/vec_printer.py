
import sys
import vect_bytes

file = sys.argv[1]
s = int(sys.argv[2])
e = int(sys.argv[3])

with open(file, 'rb') as fhandle:
  sizes = [300]*(e-s+1)
  print(vect_bytes.read_entries(fhandle, sizes, e-s+1))
