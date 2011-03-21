#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

ext_modules = [Extension("_pattern", ["util/_pattern.c"]),
               Extension("_search", ["util/_search.c"]),]

setup(
  name = 'jquizzyva extensions',
  ext_modules = ext_modules
)
