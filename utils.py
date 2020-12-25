
def compose(funcs, arg):
    result = arg
    for func in reversed(funcs):
        result = func(result)
    return result
        