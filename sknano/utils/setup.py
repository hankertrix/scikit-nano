#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('utils', parent_package, top_path)
    config.add_subpackage('analysis')
    config.add_subpackage('geometric_shapes')
    #config.add_subpackage('md_tools')
    config.add_subpackage('symmetry_groups')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
