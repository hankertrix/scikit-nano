# -*- coding: utf-8 -*-
"""
===============================================================================
Base crystallography classes (:mod:`sknano.core.crystallography._base`)
===============================================================================

.. currentmodule:: sknano.core.crystallography._base

"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals
# from builtins import object
from builtins import super
# from future.utils import with_metaclass

__docformat__ = 'restructuredtext en'

# from abc import ABCMeta, abstractproperty
from enum import Enum

# from sknano.core import rezero_array
from sknano.core.math import Vector

import numpy as np

__all__ = ['CrystalLattice', 'CrystalStructure']


class ReciprocalLatticeVectors:
    pass


class ReciprocalLattice:
    pass


class CrystalCell:
    pass


# def compute_ortho_matrix(a, b, c, alpha, beta, gamma):
#     cos_alpha = np.cos(np.radians(alpha))
#     cos_beta = np.cos(np.radians(beta))
#     cos_gamma = np.cos(np.radians(gamma))

#     sin_alpha = np.sin(np.radians(alpha))
#     sin_beta = np.sin(np.radians(beta))
#     sin_gamma = np.sin(np.radians(gamma))

#     m11 = a
#     m12 = b * cos_gamma
#     m13 = c * cos_beta

#     m22 = self.b * self.sin_gamma
#     m23 = self.c * (self.cos_alpha - self.cos_beta * self.cos_gamma) / \
#         self.sin_gamma

#     m33 = self.c * self.sin_alpha * self.sin_beta * self.sin_gamma_star / \
#         self.sin_gamma

#     return np.matrix([[m11, m12, m13],
#                       [0.0, m22, m23],
#                       [0.0, 0.0, m33]])


class CrystalLattice:
    """Base class for crystal lattice systems."""

    def __init__(self, a=None, b=None, c=None,
                 alpha=None, beta=None, gamma=None,
                 a1=None, a2=None, a3=None, cell_matrix=None,
                 orientation_matrix=None):

        self.offset = Vector(np.zeros(3))

        if orientation_matrix is None:
            orientation_matrix = np.matrix(np.identity(3))

        self.orientation_matrix = orientation_matrix

        if a1 is not None and a2 is not None and a3 is not None:
            a1 = Vector(a1)
            a2 = Vector(a2)
            a3 = Vector(a3)
            a = a1.length
            b = a2.length
            c = a3.length
            alpha = np.degrees(a2.angle(a3))
            beta = np.degrees(a3.angle(a1))
            gamma = np.degrees(a1.angle(a2))
            cell_matrix = np.matrix(np.vstack((np.asarray(a1),
                                               np.asarray(a2),
                                               np.asarray(a3))))

        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        if cell_matrix is not None:
            self.orientation_matrix = \
                cell_matrix.T * np.linalg.inv(self.ortho_matrix)

        self.lattice_type = None

        self.pstr = "a={a!r}, b={b!r}, c={c!r}, " + \
            "alpha={alpha!r}, beta={beta!r}, gamma={gamma!r}"

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               self.pstr.format(**self.pdict()))

    def pdict(self):
        """Return `dict` of `CrystalLattice` parameters."""
        return dict(a=self.a, b=self.b, c=self.c,
                    alpha=self.alpha, beta=self.beta, gamma=self.gamma)

    @classmethod
    def from_matrix(cls, cell_matrix):
        return cls.__init__(a1=cell_matrix[0,:],
                            a2=cell_matrix[1,:],
                            a3=cell_matrix[2,:])

    # @property
    # def α(self):
    #     return self.alpha

    @property
    def alpha(self):
        """Angle between lattice vectors :math:`\\mathbf{b}` and \
        :math:`\\mathbf{c}`."""
        return np.around(self._alpha, decimals=6)

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    @property
    def beta(self):
        """Angle between lattice vectors :math:`\\mathbf{c}` and \
        :math:`\\mathbf{a}`."""
        return np.around(self._beta, decimals=6)

    @beta.setter
    def beta(self, value):
        self._beta = value

    @property
    def gamma(self):
        """Angle between lattice vectors :math:`\\mathbf{a}` and \
        :math:`\\mathbf{b}`."""
        return np.around(self._gamma, decimals=6)

    @gamma.setter
    def gamma(self, value):
        self._gamma = value

    @property
    def cos_alpha(self):
        return np.around(np.cos(np.radians(self.alpha)), decimals=6)

    @property
    def cos_beta(self):
        return np.around(np.cos(np.radians(self.beta)), decimals=6)

    @property
    def cos_gamma(self):
        return np.around(np.cos(np.radians(self.gamma)), decimals=6)

    @property
    def sin_alpha(self):
        return np.around(np.sin(np.radians(self.alpha)), decimals=6)

    @property
    def sin_beta(self):
        return np.around(np.sin(np.radians(self.beta)), decimals=6)

    @property
    def sin_gamma(self):
        return np.around(np.sin(np.radians(self.gamma)), decimals=6)

    @property
    def cos_alpha_star(self):
        return np.around((self.cos_beta * self.cos_gamma - self.cos_alpha) /
                         (self.sin_beta * self.sin_gamma), decimals=6)

    @property
    def cos_beta_star(self):
        return np.around((self.cos_gamma * self.cos_alpha - self.cos_beta) /
                         (self.sin_gamma * self.sin_alpha), decimals=6)

    @property
    def cos_gamma_star(self):
        return np.around((self.cos_alpha * self.cos_beta - self.cos_gamma) /
                         (self.sin_alpha * self.sin_beta), decimals=6)

    @property
    def sin_alpha_star(self):
        return np.sqrt(1 - self.cos_alpha_star ** 2)

    @property
    def sin_beta_star(self):
        return np.sqrt(1 - self.cos_beta_star ** 2)

    @property
    def sin_gamma_star(self):
        return np.sqrt(1 - self.cos_gamma_star ** 2)

    @property
    def unit_cell(self):
        pass

    @property
    def a1(self):
        return self.ortho_matrix[:, 0].flatten()

    @property
    def a2(self):
        return self.ortho_matrix[:, 1].flatten()

    @property
    def a3(self):
        return self.ortho_matrix[:, 2].flatten()

    @property
    def b1(self):
        return np.cross(self.a2, self.a3) / self.cell_volume

    @property
    def b2(self):
        return np.cross(self.a3, self.a1) / self.cell_volume

    @property
    def b3(self):
        return np.cross(self.a1, self.a2) / self.cell_volume

    def fractional_to_cartesian(self, v):
        v = np.matrix(np.asarray(v).reshape(3, 1))
        return self.orientation_matrix * self.ortho_matrix * v + self.offset

    def cartesian_to_fractional(self, v):
        pass

    def wrap_fractional_coordinate(self):
        pass

    def wrap_cartesian_coordinate(self):
        pass

    def generate_cell_vectors(self):
        pass
        # self.a1.x = self.a
        # self.a2.x = self.b * np.cos(self.gamma)

    def space_group(self):
        pass

    @property
    def lattice_type(self):
        return self._lattice_type

    @lattice_type.setter
    def lattice_type(self, value):
        self._lattice_type = value

    def lattice_vectors(self):
        pass

    def cell_vectors(self):
        pass

    def cell_matrix(self):
        pass

    @property
    def ortho_matrix(self):
        m11 = self.a
        m12 = self.b * self.cos_gamma
        m13 = self.c * self.cos_beta

        m22 = self.b * self.sin_gamma
        m23 = self.c * (self.cos_alpha - self.cos_beta * self.cos_gamma) / \
            self.sin_gamma

        m33 = self.c * self.sin_alpha * self.sin_beta * self.sin_gamma_star / \
            self.sin_gamma

        return np.around(np.matrix([[m11, m12, m13],
                                    [0.0, m22, m23],
                                    [0.0, 0.0, m33]]), decimals=10)

    @property
    def fractional_matrix(self):
        return np.linalg.inv(self.ortho_matrix)

    @property
    def cell_volume(self):
        return self.a * self.b * self.c * \
            np.sqrt(1 - self.cos_alpha ** 2 - self.cos_beta ** 2 -
                    self.cos_gamma ** 2 +
                    2 * self.cos_alpha * self.cos_beta * self.cos_gamma)

    def origin(self):
        pass


class CrystalStructure(CrystalLattice):
    """Abstract base class for crystal structures."""

    def __init__(self, basis, **kwargs):
        super().__init__(**kwargs)
        self.basis = basis

        self.pstr = "basis={basis!r}"
        for k, v in kwargs.items():
            self.pstr += ", {}={{{key!s}!r}}".format(k, key=k)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               self.pstr.format(**self.pdict()))

    @property
    def basis(self):
        """Crystal structure basis."""
        return self._basis

    @basis.setter
    def basis(self, value):
        self._basis = value

    @basis.deleter
    def basis(self):
        del self._basis

    @property
    def unit_cell(self):
        pass

    def pdict(self):
        """Return `dict` of `CrystalStructure` parameters."""
        super_pdict = super().pdict()
        super_pdict.update(dict(basis=self.basis))
        return super_pdict
