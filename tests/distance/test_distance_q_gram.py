# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.tests.distance.test_distance_q_gram.

This module contains unit tests for abydos.distance.QGram
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import QGram


class QGramTestCases(unittest.TestCase):
    """Test QGram functions.

    abydos.distance.QGram
    """

    cmp = QGram()

    def test_q_gram_dist(self):
        """Test abydos.distance.QGram.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), float('nan'))
        self.assertEqual(self.cmp.dist('a', ''), float('nan'))
        self.assertEqual(self.cmp.dist('', 'a'), float('nan'))
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 1.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 0.8571428571)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 0.8571428571)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 0.8571428571)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 0.8571428571)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 0.4545454545
        )

    def test_q_gram_dist_abs(self):
        """Test abydos.distance.QGram.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 0)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 0)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 2)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 2)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 6)

        self.assertAlmostEqual(self.cmp.dist_abs('Nigel', 'Niall'), 6)
        self.assertAlmostEqual(self.cmp.dist_abs('Niall', 'Nigel'), 6)
        self.assertAlmostEqual(self.cmp.dist_abs('Colin', 'Coiln'), 6)
        self.assertAlmostEqual(self.cmp.dist_abs('Coiln', 'Colin'), 6)
        self.assertAlmostEqual(self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), 5)


if __name__ == '__main__':
    unittest.main()