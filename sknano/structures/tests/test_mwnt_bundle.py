# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import nose
from nose.tools import *
from sknano.structures import MWNTBundle


def test1():
    bundle = MWNTBundle(Ch=[(5, 5), (10, 10)])
    assert_equal(bundle.Nwalls, 2)


def test2():
    bundle = MWNTBundle(max_shells=5)
    assert_equal(bundle.Nwalls, 5)


if __name__ == '__main__':
    nose.runmodule()
