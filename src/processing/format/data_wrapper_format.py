
from functools import update_wrapper


class DataFormat:
    """ Value dispatch function decorator.

    Transforms a function into a value dispatch function, which can have
    different behaviors based on the value of its first argument.
    """
    def __init__(self, func):
        self.func = func
        self.registry = {}
        update_wrapper(self, func)
        # try:
        #     update_wrapper(self, function)
        # except:
        #     pass

    def format(self, value, func=None):
        if func is None:
            return lambda f: self.format(value, f)
        self.registry[value] = func
        return func

    def __call__(self, *args, **kwargs):
        return self.registry.get(args[0], self.func)(*args, **kwargs)

    def __reduce__(self):
        return self.func.__qualname__
