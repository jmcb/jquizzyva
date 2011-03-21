#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("_pattern", ["_pattern.pyx"])]

setup(
  name = '_pattern',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
