#!/usr/bin/env python

try:
    from util._memoize import Memoizer
except:
    from functools import partial

    class Memoizer (object):
        def __init__ (self, function):
            self.hash = {}

            self.function = function

            self.__name__ = function.__name__
            self.__doc__ = function.__doc__

        def __get__ (self, obj, objtype):
            return partial(self.__call__, obj)

        def __call__ (self, word):
            try:
                return self.hash[word]
            except KeyError:
                r = self.function(word)
                self.hash[word] = r
                return r
