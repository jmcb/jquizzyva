#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("_pattern", ["_pattern.pyx"]),
               Extension("_memoize", ["_memoize.pyx"])]

setup(
  name = 'jquizzyva extensions',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
