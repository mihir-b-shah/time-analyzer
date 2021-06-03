
from itertools import chain
import os

def compose(funcs, arg):
    result = arg
    for func in funcs:
        result = func(result)
    return result

def flatmap(f, items):
    return chain.from_iterable(map(f, items))

def get_path(path):
  return os.path.abspath(path)
