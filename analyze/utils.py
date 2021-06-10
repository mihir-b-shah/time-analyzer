
from itertools import chain
import os
import re

def compose(funcs, arg):
    result = arg
    for func in funcs:
        result = func(result)
    return result

def flatmap(f, items):
    return chain.from_iterable(map(f, items))

def get_path(path):
  return os.path.abspath(path)

def log(categ, msg):
  f = open('log.txt', 'a')
  f.write('%s: %s\n'%(categ.upper(), re.sub(r'\s+', ' ', msg)))
  f.close()
