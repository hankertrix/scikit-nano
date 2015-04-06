#!/usr/bin/env python
from __future__ import division, print_function, absolute_import
from __future__ import unicode_literals


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('scripts', parent_package, top_path)
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
