# -*- coding: utf-8 -*-
"""
===========================================================================
Crystal cell classes (:mod:`sknano.core.crystallography.xtal_cells`)
===========================================================================

.. currentmodule:: sknano.core.crystallography.xtal_cells

"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals
__docformat__ = 'restructuredtext en'

from functools import total_ordering
# import copy
import numbers

import numpy as np

from sknano.core import BaseClass, TabulateMixin
from sknano.core.atoms import BasisAtom, BasisAtoms
from .extras import supercell_lattice_points

__all__ = ['CrystalCell', 'UnitCell', 'SuperCell']


@total_ordering
class UnitCell(BaseClass, TabulateMixin):
    """Base class for abstract representations of crystallographic unit cells.

    Parameters
    ----------
    lattice : :class:`~sknano.core.crystallography.LatticeBase` sub-class
    basis : {:class:`~python:list`, :class:`~sknano.core.atoms.BasisAtoms`}
    coords : {:class:`~python:list`}, optional
    cartesian : {:class:`~python:bool`}, optional
    wrap_coords : {:class:`~python:bool`}, optional

    """

    def __init__(self, lattice=None, basis=None, coords=None, cartesian=False,
                 wrap_coords=False):

        super().__init__()

        if basis is None:
            basis = BasisAtoms()
        else:
            basis = BasisAtoms(basis)
            if lattice is not None:
                basis.lattice = lattice
                if coords is not None and len(basis) == len(coords):
                    for atom, pos in zip(basis, coords):
                        atom.lattice = lattice
                        if not cartesian:
                            atom.rs = pos
                        else:
                            atom.rs = lattice.cartesian_to_fractional(pos)

        self.lattice = lattice
        self.basis = basis
        self.wrap_coords = wrap_coords
        self.fmtstr = "{lattice!r}, {basis!r}, {coords!r}, " + \
            "cartesian=False, wrap_coords={wrap_coords!r}"

    def __str__(self):
        strrep = self._table_title_str()
        objstr = self._obj_mro_str()
        lattice = self.lattice
        if lattice is not None:
            title = '.'.join((objstr, lattice.__class__.__qualname__))
            strrep = '\n'.join((strrep, title, str(lattice)))
        basis = self.basis
        if basis.data:
            title = '.'.join((objstr, basis.__class__.__qualname__))
            strrep = '\n'.join((strrep, title, str(basis)))
        return strrep

    def __deepcopy__(self, memo):
        obj = self.__class__(**self.todict())
        memo[id(self)] = obj
        return obj

    def __dir__(self):
        return ['lattice', 'basis']

    def __eq__(self, other):
        return self is other or \
            all([(getattr(self, attr) == getattr(other, attr)) for attr
                 in dir(self)])

    def __lt__(self, other):
        return (self.lattice < other.lattice and self.basis <= other.basis) \
            or (self.lattice <= other.lattice and self.basis < other.basis)

    def __getattr__(self, name):
        try:
            return getattr(self.lattice, name)
        except AttributeError:
            try:
                return getattr(self.basis, name)
            except AttributeError:
                return super().__getattr__(name)

    def __iter__(self):
        return iter(self.basis)

    # @property
    # def basis(self):
    #     return self._basis

    # @basis.setter
    # def basis(self, value):
    #     lattice = self.lattice
    #     coords = self.coords
    #     if value is None:
    #         value = BasisAtoms()
    #     elif value is not None:
    #         value = BasisAtoms(value, lattice=lattice)
    #         if coords is not None:
    #             for atom, pos in zip(basis, coords):
    #                 atom.lattice = lattice
    #                 if not cartesian:
    #                     atom.rs = pos
    #                 else:
    #                     atom.rs = lattice.cartesian_to_fractional(pos)

    def rotate(self, **kwargs):
        """Rotate unit cell lattice vectors and basis."""
        if kwargs.get('anchor_point', None) is None:
            kwargs['anchor_point'] = self.lattice.offset
        self.lattice.rotate(**kwargs)
        self.basis.rotate(**kwargs)

    def translate(self, t, fix_anchor_points=True):
        """Translate unit cell basis."""
        self.lattice.translate(t)
        self.basis.translate(t, fix_anchor_points=fix_anchor_points)

    def todict(self):
        """Return `dict` of :class:`UnitCell` parameters."""
        return dict(lattice=self.lattice, basis=self.basis.symbols.tolist(),
                    coords=self.basis.rs.tolist(),
                    wrap_coords=self.wrap_coords)


@total_ordering
class CrystalCell(BaseClass, TabulateMixin):
    """Class representation of crystal structure cell.

    Parameters
    ----------
    lattice : :class:`~sknano.core.crystallography.LatticeBase` sub-class
    basis : {:class:`~python:list`, :class:`~sknano.core.atoms.BasisAtoms`}
    coords : {:class:`~python:list`}, optional
    cartesian : {:class:`~python:bool`}, optional
    wrap_coords : {:class:`~python:bool`}, optional
    unit_cell : :class:`~sknano.core.crystallography.UnitCell`
    scaling_matrix : {:class:`~python:int`, :class:`~python:list`}

    """

    def __init__(self, lattice=None, basis=None, coords=None, cartesian=False,
                 wrap_coords=False, unit_cell=None, scaling_matrix=None):
        super().__init__()

        # if unit_cell is None and basis is not None:
        if basis is not None:
            basis = BasisAtoms(basis)
            if lattice is not None:
                basis.lattice = lattice
                if coords is not None and len(basis) == len(coords):
                    for atom, pos in zip(basis, coords):
                        atom.lattice = lattice
                        if not cartesian:
                            atom.rs = pos
                        else:
                            atom.rs = lattice.cartesian_to_fractional(pos)

        # if basis is None:
        #     basis = BasisAtoms()

        # These attributes may be reset in the `@scaling_matrix.setter`
        # method and so they need to be initialized *before* setting
        # `self.scaling_matrix`.
        self.basis = basis
        self.lattice = lattice

        self.unit_cell = unit_cell
        self.wrap_coords = wrap_coords
        self.scaling_matrix = scaling_matrix

        self.fmtstr = \
            "lattice={lattice!r}, basis={basis!r}, coords={coords!r}, " + \
            "cartesian=False, wrap_coords={wrap_coords!r}, " + \
            "unit_cell={unit_cell!r}, scaling_matrix={scaling_matrix!r}"

    def __deepcopy__(self, memo):
        obj = self.__class__(**self.todict())
        memo[id(self)] = obj
        return obj

    def __dir__(self):
        return ['lattice', 'basis', 'unit_cell', 'scaling_matrix']

    def __str__(self):
        strrep = self._table_title_str()
        objstr = self._obj_mro_str()
        lattice = self.lattice
        unit_cell = self.unit_cell
        if lattice is not None:
            title = '.'.join((objstr, lattice.__class__.__qualname__))
            strrep = '\n'.join((strrep, title, str(lattice)))
        if unit_cell is not None:
            title = '.'.join((objstr, unit_cell.__class__.__qualname__))
            strrep = '\n'.join((strrep, title, str(unit_cell)))
        basis = self.basis
        if isinstance(basis, BasisAtoms) and basis.data:
            title = '.'.join((objstr, basis.__class__.__qualname__))
            strrep = '\n'.join((strrep, title, str(basis)))
        return strrep

    def __eq__(self, other):
        if all([attr is not None for attr in
                (self.scaling_matrix, self.unit_cell,
                 other.scaling_matrix, other.unit_cell)]) and \
                self.scaling_matrix.shape == other.scaling_matrix.shape:
            return self is other or \
                (self.unit_cell == other.unit_cell and
                 np.allclose(self.scaling_matrix, other.scaling_matrix))
        elif all([cell is not None for cell in
                  (self.unit_cell, other.unit_cell)]):
            return self is other or \
                (self.unit_cell == other.unit_cell and
                 all([mat is None for mat in
                      (self.scaling_matrix, other.scaling_matrix)]))

    def __lt__(self, other):
        return (self.unit_cell < other.unit_cell and
                self.scaling_matrix <= other.scaling_matrix) \
            or (self.unit_cell <= other.unit_cell and
                self.scaling_matrix < other.scaling_matrix)

    def __iter__(self):
        """Return iterator over the :attr:`CrystalCell.basis`."""
        return iter(self.basis)

    def __getattr__(self, name):
        if name != 'lattice' and self.lattice is not None:
            try:
                return getattr(self.lattice, name)
            except AttributeError:
                pass
        if name != 'basis' and self.basis is not None and len(self.basis) != 0:
            try:
                return getattr(self.basis, name)
            except AttributeError:
                pass
        try:
            return getattr(self.unit_cell, name)
        except AttributeError:
            return super().__getattr__(name)

    @property
    def basis(self):
        """:class:`~sknano.core.atoms.BasisAtoms`."""
        return self._basis

    @basis.setter
    def basis(self, value):
        self._basis = value
        # if self.unit_cell is not None:
        #     self.unit_cell.basis[:] = \
        #         self.basis[:self.unit_cell.basis.Natoms]

    @property
    def lattice(self):
        """:class:`~sknano.core.crystallography.CrystalLattice`."""
        return self._lattice

    @lattice.setter
    def lattice(self, value):
        self._lattice = value
        if self.basis is not None:
            self.basis.lattice = self.lattice

    @property
    def unit_cell(self):
        """:class:`UnitCell`."""
        return self._unit_cell

    @unit_cell.setter
    def unit_cell(self, value):
        if value is not None and not isinstance(value, UnitCell):
            raise ValueError('Expected a `UnitCell` object')
        self._unit_cell = value
        if value is not None:
            if self.basis is None:
                self._basis = self.unit_cell.basis
            if self.lattice is None:
                self._lattice = self.unit_cell.lattice
            # if self.lattice is None:
            #     self._lattice = self.unit_cell.lattice
            # if self.basis is None or self.basis.Natoms == 0:
            #     self._basis = self.unit_cell.basis

    @property
    def scaling_matrix(self):
        """Scaling matrix."""
        return self._scaling_matrix

    @scaling_matrix.setter
    def scaling_matrix(self, value):
        if value is None:
            self._scaling_matrix = np.asmatrix(np.eye(3, dtype=int))
            return

        if not isinstance(value, (int, float, tuple, list, np.ndarray)):
            return

        if self.lattice is None:
            return

        if isinstance(value, np.ndarray) and \
                ((value.shape == np.ones(3).shape and
                  np.allclose(value, np.ones(3))) or
                 (value.shape == np.eye(3).shape and
                  np.allclose(value, np.eye(3)))):
            self._scaling_matrix = np.asmatrix(value)
            return

        if isinstance(value, numbers.Number):
            value = self.lattice.nd * [int(value)]

        scaling_matrix = np.asmatrix(value, dtype=int)
        # scaling_matrix = np.asmatrix(value)
        if scaling_matrix.shape != self.lattice.matrix.shape:
            scaling_matrix = np.diagflat(scaling_matrix)
        self._scaling_matrix = scaling_matrix

        self.lattice = self.lattice.__class__(
            cell_matrix=self.scaling_matrix * self.lattice.matrix)

        tvecs = \
            np.asarray(
                np.asmatrix(supercell_lattice_points(self.scaling_matrix)) *
                self.lattice.matrix)

        basis = self.basis[:]
        max_mol = max(set(basis.mols))
        self.basis = BasisAtoms()
        for atom in basis:
            for i, tvec in enumerate(tvecs):
                xs, ys, zs = \
                    self.lattice.cartesian_to_fractional(atom.r + tvec)
                if self.wrap_coords:
                    xs, ys, zs = \
                        self.lattice.wrap_fractional_coordinate(
                            [xs, ys, zs])
                mol = i * max_mol + atom.mol
                self.basis.append(BasisAtom(atom.element,
                                            mol=mol, id=atom.id,
                                            lattice=self.lattice,
                                            xs=xs, ys=ys, zs=zs))

    def rezero(self, **kwargs):
        """Rezero the crystal cell basis coordinates."""
        if self.basis is not None:
            self.basis.rezero(**kwargs)

    def rotate(self, **kwargs):
        """Rotate crystal cell lattice, basis, and unit cell."""
        if kwargs.get('anchor_point', None) is None:
            kwargs['anchor_point'] = self.lattice.offset
        if self.lattice is not None:
            self.lattice.rotate(**kwargs)
        if self.basis is not None:
            self.basis.rotate(**kwargs)
        if self.unit_cell is not None:
            self.unit_cell.rotate(**kwargs)

    def translate(self, t, fix_anchor_points=True):
        """Translate crystal cell lattice, basis, and unit cell."""
        if self.lattice is not None:
            self.lattice.translate(t)
        if self.basis is not None:
            self.basis.translate(t, fix_anchor_points=fix_anchor_points)
        if self.unit_cell is not None:
            self.unit_cell.translate(t, fix_anchor_points=fix_anchor_points)

    def translate_basis(self, t, cartesian=True, wrap_coords=True):
        """Translate the crystal cell basis."""
        if cartesian:
            t = self.lattice.cartesian_to_fractional(t)

        basis = self.basis[:]
        self.basis = BasisAtoms()

        for atom in basis:
            xs, ys, zs = atom.rs + t
            if wrap_coords:
                xs, ys, zs = \
                    self.lattice.wrap_fractional_coordinate([xs, ys, zs])
            self.basis.append(BasisAtom(atom.element,
                                        mol=atom.mol, id=atom.id,
                                        lattice=self.lattice,
                                        xs=xs, ys=ys, zs=zs))

    def update_basis(self, element, index=None, step=None):
        """Update a crystal cell basis element."""
        if index is None:
            [self.unit_cell.basis.__setitem__(i, element)
             for i in range(len(self.unit_cell.basis))]
            [self.basis.__setitem__(i, element)
             for i in range(len(self.basis))]
        elif isinstance(index, int):
            if step is None:
                step = self.unit_cell.basis.Natoms
            [self.unit_cell.basis.__setitem__(i, element)
             for i in range(index, len(self.unit_cell.basis), step)]
            [self.basis.__setitem__(i, element)
             for i in range(index, len(self.basis), step)]
        elif isinstance(index, (list, np.ndarray)):
            [self.unit_cell.basis.__setitem__(i, element) for i in index]
            [self.basis.__setitem__(i, element) for i in index]

    def update_lattice_and_basis(self, to_unit_cell=False,
                                 from_unit_cell=None):
        """Update/set the crystal cell lattice and basis."""
        if to_unit_cell:
            if self.unit_cell is not None:
                self._basis = self.unit_cell.basis
                self._lattice = self.unit_cell.lattice
        elif from_unit_cell is not None:
            self._basis = from_unit_cell.basis
            self._lattice = from_unit_cell.lattice

    def todict(self):
        """:class:`~python:dict` of :class:`CrystalCell` parameters."""
        try:
            return dict(lattice=self.lattice,
                        basis=self.basis.symbols.tolist(),
                        coords=self.basis.rs.tolist(),
                        wrap_coords=self.wrap_coords,
                        unit_cell=self.unit_cell,
                        scaling_matrix=self.scaling_matrix.tolist())
        except AttributeError:
            return dict(lattice=self.lattice, basis=None, coords=None,
                        wrap_coords=self.wrap_coords,
                        unit_cell=self.unit_cell,
                        scaling_matrix=self.scaling_matrix.tolist())


class SuperCell(CrystalCell):
    """Class representation of crystal structure supercell.

    Parameters
    ----------
    unit_cell : :class:`~sknano.core.crystallography.UnitCell`
    scaling_matrix : {:class:`~python:int`, :class:`~python:list`}

    """

    def __init__(self, unit_cell, scaling_matrix, wrap_coords=False):
        if not isinstance(unit_cell, UnitCell):
            raise ValueError('Expected a `UnitCell` for `unit_cell`.')
        if not isinstance(scaling_matrix,
                          (int, float, tuple, list, np.ndarray)):
            raise ValueError('Expected an `int` or `array_like` object of\n'
                             'integers for `scaling_matrix`')
        super().__init__(unit_cell=unit_cell, scaling_matrix=scaling_matrix,
                         wrap_coords=wrap_coords)
