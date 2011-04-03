#!/usr/bin/env python

from functools import partial

class Memoizer (object):
    def __init__ (self, function, pattern):
        self.hash = {}

        self.function = function
        self.pattern = pattern

        self.__name__ = function.__name__
        self.__doc__ = function.__doc__

    def __get__ (self, obj, objtype):
        return partial(self.__call__, obj)

    def __call__ (self, word):
        try:
            result = self.hash[word]
        except KeyError:
            r = self.function(word)
            self.hash[word] = r
            return r[0]
        else:
            if result[0]:
                self.pattern.blank_store.append(result[1])

            return result[0]
