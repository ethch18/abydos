# Copyright 2014-2020 by Christopher C. Little.
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

"""abydos.tests.distance.test_distance_prefix.

This module contains unit tests for abydos.distance.Prefix
"""

import unittest

from abydos.distance import Prefix, dist_prefix, sim_prefix


class PrefixTestCases(unittest.TestCase):
    """Test prefix similarity functions.

    abydos.distance.Prefix
    """

    cmp = Prefix()

    def test_prefix_sim(self):
        """Test abydos.distance.Prefix.sim."""
        self.assertEqual(self.cmp.sim('', ''), 1)
        self.assertEqual(self.cmp.sim('a', ''), 0)
        self.assertEqual(self.cmp.sim('', 'a'), 0)
        self.assertEqual(self.cmp.sim('a', 'a'), 1)
        self.assertEqual(self.cmp.sim('ax', 'a'), 1)
        self.assertEqual(self.cmp.sim('axx', 'a'), 1)
        self.assertEqual(self.cmp.sim('ax', 'ay'), 1 / 2)
        self.assertEqual(self.cmp.sim('a', 'ay'), 1)
        self.assertEqual(self.cmp.sim('a', 'ayy'), 1)
        self.assertEqual(self.cmp.sim('ax', 'ay'), 1 / 2)
        self.assertEqual(self.cmp.sim('a', 'y'), 0)
        self.assertEqual(self.cmp.sim('y', 'a'), 0)
        self.assertEqual(self.cmp.sim('aaax', 'aaa'), 1)
        self.assertAlmostEqual(self.cmp.sim('axxx', 'aaa'), 1 / 3)
        self.assertEqual(self.cmp.sim('aaxx', 'aayy'), 1 / 2)
        self.assertEqual(self.cmp.sim('xxaa', 'yyaa'), 0)
        self.assertAlmostEqual(self.cmp.sim('aaxxx', 'aay'), 2 / 3)
        self.assertEqual(self.cmp.sim('aaxxxx', 'aayyy'), 2 / 5)
        self.assertEqual(self.cmp.sim('xa', 'a'), 0)
        self.assertEqual(self.cmp.sim('xxa', 'a'), 0)
        self.assertEqual(self.cmp.sim('xa', 'ya'), 0)
        self.assertEqual(self.cmp.sim('a', 'ya'), 0)
        self.assertEqual(self.cmp.sim('a', 'yya'), 0)
        self.assertEqual(self.cmp.sim('xa', 'ya'), 0)
        self.assertEqual(self.cmp.sim('xaaa', 'aaa'), 0)
        self.assertEqual(self.cmp.sim('xxxa', 'aaa'), 0)
        self.assertEqual(self.cmp.sim('xxxaa', 'yaa'), 0)
        self.assertEqual(self.cmp.sim('xxxxaa', 'yyyaa'), 0)

        # Test wrapper
        self.assertEqual(sim_prefix('aaxxxx', 'aayyy'), 2 / 5)

    def test_prefix_dist(self):
        """Test abydos.distance.Prefix.dist."""
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 1)
        self.assertEqual(self.cmp.dist('', 'a'), 1)
        self.assertEqual(self.cmp.dist('a', 'a'), 0)
        self.assertEqual(self.cmp.dist('ax', 'a'), 0)
        self.assertEqual(self.cmp.dist('axx', 'a'), 0)
        self.assertEqual(self.cmp.dist('ax', 'ay'), 1 / 2)
        self.assertEqual(self.cmp.dist('a', 'ay'), 0)
        self.assertEqual(self.cmp.dist('a', 'ayy'), 0)
        self.assertEqual(self.cmp.dist('ax', 'ay'), 1 / 2)
        self.assertEqual(self.cmp.dist('a', 'y'), 1)
        self.assertEqual(self.cmp.dist('y', 'a'), 1)
        self.assertEqual(self.cmp.dist('aaax', 'aaa'), 0)
        self.assertAlmostEqual(self.cmp.dist('axxx', 'aaa'), 2 / 3)
        self.assertEqual(self.cmp.dist('aaxx', 'aayy'), 1 / 2)
        self.assertEqual(self.cmp.dist('xxaa', 'yyaa'), 1)
        self.assertAlmostEqual(self.cmp.dist('aaxxx', 'aay'), 1 / 3)
        self.assertEqual(self.cmp.dist('aaxxxx', 'aayyy'), 3 / 5)
        self.assertEqual(self.cmp.dist('xa', 'a'), 1)
        self.assertEqual(self.cmp.dist('xxa', 'a'), 1)
        self.assertEqual(self.cmp.dist('xa', 'ya'), 1)
        self.assertEqual(self.cmp.dist('a', 'ya'), 1)
        self.assertEqual(self.cmp.dist('a', 'yya'), 1)
        self.assertEqual(self.cmp.dist('xa', 'ya'), 1)
        self.assertEqual(self.cmp.dist('xaaa', 'aaa'), 1)
        self.assertEqual(self.cmp.dist('xxxa', 'aaa'), 1)
        self.assertEqual(self.cmp.dist('xxxaa', 'yaa'), 1)
        self.assertEqual(self.cmp.dist('xxxxaa', 'yyyaa'), 1)

        # Test wrapper
        self.assertEqual(dist_prefix('aaxxxx', 'aayyy'), 3 / 5)


if __name__ == '__main__':
    unittest.main()
