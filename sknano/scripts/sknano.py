#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
====================================================
Command line script (:mod:`sknano.scripts.sknano`)
====================================================

CLI to :mod:`sknano` tools.

.. currentmodule:: sknano.scripts.sknano

.. code-block:: python

   > sknano --help

.. autofunction:: sknano

Examples
--------


"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals
__docformat__ = 'restructuredtext en'

# import argparse
# import importlib
import sys

# from .parser import add_default_arguments
from .nanogen import nanogen_parser, nanogen

__all__ = ['sknano', 'sknano_parser']


def sknano_parser():
    """:mod:`~sknano.scripts.sknano` script \
        :class:`~python:argparse.ArgumentParser`."""
    return nanogen_parser()


def sknano(**kwargs):
    """:mod:`~sknano.scripts.sknano` script function."""
    nanogen(**kwargs)


def main():
    args = sknano_parser().parse_args()
    if hasattr(args, 'generator_class'):
        sknano(**vars(args))
    else:
        sknano_parser().print_help()


if __name__ == '__main__':
    sys.exit(main())
