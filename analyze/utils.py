
from itertools import chain

def compose(funcs, arg):
    result = arg
    for func in funcs:
        result = func(result)
    return result

def flatmap(f, items):
    return chain.from_iterable(map(f, items))