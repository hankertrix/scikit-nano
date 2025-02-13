# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import warnings
warnings.simplefilter('always')

import nose
from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_is_instance
from sknano.core.atoms import BasisAtoms
from sknano.core.crystallography import CrystalCell, UnitCell
from sknano.core.structures import SWNT


def test1():
    swnt = SWNT(n=10, m=10)
    assert_is_instance(swnt.todict(), dict)
    assert_true('n1' not in swnt.todict())
    assert_equal(swnt.n, 10)
    assert_equal(swnt.m, 10)
    assert_equal(swnt.element1, 'C')
    assert_equal(swnt.element2, 'C')
    assert_equal(swnt.n3, 1.0)
    assert_equal(swnt.t1, 1)
    assert_equal(swnt.t2, -1)
    assert_equal(swnt.d, 10)
    assert_equal(swnt.dR, 30)
    assert_equal(swnt.N, 20)
    assert_equal(swnt.R, (1, 0))
    assert_almost_equal(swnt.chiral_angle, 30.0)
    assert_almost_equal(swnt.Ch, 42.6, places=2)
    assert_almost_equal(swnt.T, 2.46, places=2)
    assert_almost_equal(swnt.dt, 13.56, places=2)
    assert_almost_equal(swnt.rt, 6.78, places=2)
    assert_equal(swnt.Ntubes, 1)


def test2():
    swnt = SWNT(n=20, m=10)
    assert_equal(swnt.element1, 'C')
    assert_equal(swnt.element2, 'C')
    assert_equal(swnt.n, 20)
    assert_equal(swnt.m, 10)
    assert_equal(swnt.n3, 1.0)
    assert_equal(swnt.t1, 4)
    assert_equal(swnt.t2, -5)
    assert_equal(swnt.d, 10)
    assert_equal(swnt.dR, 10)
    assert_equal(swnt.N, 140)
    assert_equal(swnt.R, (1, -1))
    assert_almost_equal(swnt.chiral_angle, 19.11, places=2)
    assert_almost_equal(swnt.Ch, 65.07, places=2)
    assert_almost_equal(swnt.T, 11.27, places=2)
    assert_almost_equal(swnt.dt, 20.71, places=2)
    assert_almost_equal(swnt.rt, 10.36, places=2)
    assert_equal(swnt.Ntubes, 1)


def test3():
    swnt = SWNT(n=20, m=0)
    assert_equal(swnt.element1, 'C')
    assert_equal(swnt.element2, 'C')
    assert_equal(swnt.n, 20)
    assert_equal(swnt.m, 0)
    assert_equal(swnt.n3, 1.0)
    assert_equal(swnt.t1, 1)
    assert_equal(swnt.t2, -2)
    assert_equal(swnt.d, 20)
    assert_equal(swnt.dR, 20)
    assert_equal(swnt.N, 40)
    assert_equal(swnt.R, (1, -1))
    assert_almost_equal(swnt.chiral_angle, 0.0, places=2)
    assert_almost_equal(swnt.Ch, 49.2, places=1)
    assert_almost_equal(swnt.T, 4.26, places=2)
    assert_almost_equal(swnt.dt, 15.7, places=1)
    assert_almost_equal(swnt.rt, 7.8, places=1)
    assert_equal(swnt.Ntubes, 1)


def test4():
    swnt = SWNT((10, 5))

    assert_equal(swnt.element1, 'C')
    assert_equal(swnt.element2, 'C')
    assert_is_instance(swnt.basis, list)
    assert_is_instance(swnt.unit_cell, UnitCell)
    assert_is_instance(swnt.crystal_cell, CrystalCell)
    assert_is_instance(swnt.crystal_cell.basis, BasisAtoms)
    assert_equal(swnt.basis[:2], ['C', 'C'])

    swnt.element1 = 'N'
    assert_equal(swnt.element1, 'N')
    swnt.element2 = 'Ar'
    assert_equal(swnt.element2, 'Ar')
    assert_equal(swnt.unit_cell.basis.symbols.tolist()[:2], ['N', 'Ar'])
    assert_equal(swnt.crystal_cell.basis.symbols.tolist()[:2], ['N', 'Ar'])
    assert_equal(swnt.basis, ['N', 'Ar'])


def test5():
    swnt = SWNT((10, 5), basis=['B', 'N'])
    assert_equal(swnt.element1, 'B')
    assert_equal(swnt.element2, 'N')
    basis_symbols = swnt.unit_cell.basis.symbols.tolist()
    print('swnt.unit_cell.basis.symbols.tolist():\n{}'.format(basis_symbols))
    assert_equal(swnt.unit_cell.basis.symbols.tolist(),
                 swnt.N * ['B', 'N'])
    assert_equal(swnt.unit_cell.basis.symbols.tolist()[:2], ['B', 'N'])
    assert_is_instance(swnt.unit_cell.basis, BasisAtoms)

    swnt.element1 = 'N'
    swnt.element2 = 'B'

    assert_equal(swnt.element1, 'N')
    assert_equal(swnt.element2, 'B')

    assert_equal(swnt.unit_cell.basis.symbols.tolist(),
                 swnt.N * ['N', 'B'])
    assert_equal(swnt.crystal_cell.basis.symbols.tolist(),
                 swnt.N * ['N', 'B'])
    assert_equal(swnt.basis, ['N', 'B'])


def test6():
    swnt = SWNT((10, 5), element1='B', element2='N')
    assert_equal(swnt.element1, 'B')
    assert_equal(swnt.element2, 'N')
    swnt.element1 = 'N'
    swnt.element2 = 'B'
    assert_equal(swnt.element1, 'N')
    assert_equal(swnt.element2, 'B')

    assert_equal(swnt.unit_cell.basis.symbols.tolist()[:2], ['N', 'B'])
    assert_equal(swnt.crystal_cell.basis.symbols.tolist()[:2], ['N', 'B'])
    assert_equal(swnt.basis, ['N', 'B'])


def test7():
    swnt = SWNT(n=10, m=10)
    assert_equal(swnt.n, 10)
    assert_equal(swnt.m, 10)
    assert_equal(swnt.element1, 'C')
    assert_equal(swnt.element2, 'C')
    assert_equal(swnt.n3, 1.0)
    assert_equal(swnt.t1, 1)
    assert_equal(swnt.t2, -1)
    assert_equal(swnt.d, 10)
    assert_equal(swnt.dR, 30)
    assert_equal(swnt.N, 20)
    assert_equal(swnt.R, (1, 0))
    assert_almost_equal(swnt.chiral_angle, 30.0)
    assert_almost_equal(swnt.Ch, 42.6, places=2)
    assert_almost_equal(swnt.T, 2.46, places=2)
    assert_almost_equal(swnt.dt, 13.56, places=2)
    assert_almost_equal(swnt.rt, 6.78, places=2)
    assert_equal(swnt.Ntubes, 1)


def test8():
    bundle = SWNT(n=10, m=10, n1=3, n2=3)
    print(bundle.scaling_matrix)
    print(bundle.Natoms)
    assert_equal(bundle.element1, 'C')
    assert_equal(bundle.element2, 'C')
    assert_equal(bundle.Ntubes, 9)
    # print(bundle.lattice)
    assert_equal(bundle.Ntubes * bundle.unit_cell.basis.Natoms,
                 bundle.crystal_cell.basis.Natoms)


def test9():
    bundle = SWNT(n=10, m=10, n1=3, n2=3, n3=2)
    print(bundle.scaling_matrix)
    print(bundle.Natoms)
    assert_equal(bundle.element1, 'C')
    assert_equal(bundle.element2, 'C')
    assert_equal(bundle.Ntubes, 9)
    # print(bundle.lattice)
    assert_equal(bundle.Ntubes * bundle.n3 * bundle.unit_cell.basis.Natoms,
                 bundle.crystal_cell.basis.Natoms)

if __name__ == '__main__':
    nose.runmodule()
