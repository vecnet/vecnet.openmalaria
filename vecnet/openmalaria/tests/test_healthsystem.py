# -*- coding: utf-8 -*-
#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
from vecnet.openmalaria.healthsystem import get_prob_from_percentage, get_percentage_from_prob


class TestHealthSystem(unittest.TestCase):
    def setUp(self):
        pass

    def test_probabilities(self):
        # get_prob_from_percentage
        self.assertRaises(AssertionError, get_prob_from_percentage, -1)
        self.assertRaises(AssertionError, get_prob_from_percentage, 101)
        self.assertRaises(AssertionError, get_prob_from_percentage, "not a number")

        self.assertEqual(get_prob_from_percentage(50), 0.2411937)
        self.assertEqual(get_prob_from_percentage(0), 0.0)
        self.assertEqual(get_prob_from_percentage(100), 0.9984184)

        for i in range(0, 101):
            self.assertEqual(get_percentage_from_prob(get_prob_from_percentage(i)), i)

        # get_percentage_from_prob
        self.assertEqual(get_percentage_from_prob(0.5), 77)
        self.assertEqual(get_percentage_from_prob(0.0), 0)
        self.assertEqual(get_percentage_from_prob(0.003655051), 0)
        self.assertEqual(get_percentage_from_prob(0.003655053), 1)
        self.assertEqual(get_percentage_from_prob(0.01), 2)
        self.assertEqual(get_percentage_from_prob(0.5), 77)
        self.assertEqual(get_percentage_from_prob(0.9984183), 99)
        self.assertEqual(get_percentage_from_prob(0.9984185), 100)
        self.assertEqual(get_percentage_from_prob(1.00), 100)