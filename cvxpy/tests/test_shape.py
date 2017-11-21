"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from cvxpy.utilities import shape
import unittest


class TestShape(unittest.TestCase):
    """ Unit tests for the expressions/shape module. """

    def setUp(self):
        pass

    # Test adding two shapes.
    def test_add_matching(self):
        """Test addition of matching shapes.
        """
        self.assertEqual(shape.sum_shapes([(3, 4), (3, 4)]), (3, 4))
        self.assertEqual(shape.sum_shapes([(3, 4)] * 5), (3, 4))

    def test_add_broadcasting(self):
        """Test broadcasting of shapes during addition.
        """
        # Broadcasting with scalars is permitted.
        self.assertEqual(shape.sum_shapes([(3, 4), (1, 1)]), (3, 4))
        self.assertEqual(shape.sum_shapes([(1, 1), (3, 4)]), (3, 4))

        self.assertEqual(shape.sum_shapes([(1,), (3, 4)]), (3, 4))
        self.assertEqual(shape.sum_shapes([(3, 4), (1,)]), (3, 4))

        self.assertEqual(shape.sum_shapes([tuple([]), (3, 4)]), (3, 4))
        self.assertEqual(shape.sum_shapes([(3, 4), tuple([])]), (3, 4))

        self.assertEqual(shape.sum_shapes([(1, 1), (4,)]), (1, 4))
        self.assertEqual(shape.sum_shapes([(4,), (1, 1)]), (1, 4))

        # All other types of broadcasting is not permitted.
        with self.assertRaises(ValueError):
            shape.sum_shapes([(4, 1), (4,)])
        with self.assertRaises(ValueError):
            shape.sum_shapes([(4,), (4, 1)])

        with self.assertRaises(ValueError):
            shape.sum_shapes([(4, 2), (2,)])
        with self.assertRaises(ValueError):
            shape.sum_shapes([(2,), (4, 2)])

        with self.assertRaises(ValueError):
            shape.sum_shapes([(4, 2), (4, 1)])
        with self.assertRaises(ValueError):
            shape.sum_shapes([(4, 1), (4, 2)])

    def test_add_incompatible(self):
        """Test addition of incompatible shapes raises a ValueError.
        """
        with self.assertRaises(ValueError):
            shape.sum_shapes([(4, 2), (4,)])

    def test_mul_scalars(self):
        """Test multiplication by scalars raises a ValueError.
        """
        with self.assertRaises(ValueError):
            shape.mul_shapes(tuple(), (5, 9))
        with self.assertRaises(ValueError):
            shape.mul_shapes((5, 9), tuple())
        with self.assertRaises(ValueError):
            shape.mul_shapes(tuple(), tuple())

    def test_mul_2d(self):
        """Test multiplication where at least one of the shapes is >= 2D.
        """
        self.assertEqual(shape.mul_shapes((5, 9), (9, 2)), (5, 2))
        self.assertEqual(shape.mul_shapes((3, 5, 9), (3, 9, 2)), (3, 5, 2))

        with self.assertRaises(Exception) as cm:
            shape.mul_shapes((5, 3), (9, 2))
        self.assertEqual(str(cm.exception),
                         "Incompatible dimensions (5, 3) (9, 2)")

        with self.assertRaises(Exception) as cm:
            shape.mul_shapes((3, 5, 9), (4, 9, 2))
        self.assertEqual(str(cm.exception),
                         "Incompatible dimensions (3, 5, 9) (4, 9, 2)")