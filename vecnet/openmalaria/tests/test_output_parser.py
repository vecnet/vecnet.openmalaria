#!/bin/env python2
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
import math
import os

from vecnet.openmalaria.output_parser import OutputParser

base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(base_dir, "files", "test_output_parser")


class TestOutputParser(unittest.TestCase):
    def test_output_parser(self):
        output_parser = OutputParser(open(os.path.join(base_dir, "scenario.xml")),
                                     survey_output_file=open(os.path.join(base_dir, "output.txt")),
                                     cts_output_file=open(os.path.join(base_dir, "ctsout.txt")))
        self.assertEqual(output_parser.survey_time_list, [730, 803, 876, 949, 1022, 1095])
        self.assertEqual(output_parser.get_cts_measures(), ["simulated EIR"])
        self.assertEqual(len(output_parser.cts_output_data["simulated EIR"]), 1096)
        self.assertEqual(set(output_parser.get_survey_measures()), ({(3, 2), (3, 1), (14, 1), (14, 2)}))
        measure_names = set()
        for measure in output_parser.get_survey_measures():
            measure_names.add(output_parser.get_survey_measure_name(measure_id=measure[0],
                                                                    third_dimension=measure[1]))
        self.assertEqual(measure_names,
                         ({"nPatent(18 - 90)", "nPatent(0.0 - 18)", "nUncomp(0.0 - 18)", "nUncomp(18 - 90)"}))
        self.assertEqual(output_parser.survey_output_data,
                         {(3, 2): [[730, 16.0], [803, 17.0], [876, 16.0], [949, 14.0], [1022, 12.0], [1095, 10.0]],
                          (3, 1): [[730, 27.0], [803, 16.0], [876, 15.0], [949, 23.0], [1022, 20.0], [1095, 13.0]],
                          (14, 1): [[730, 1116.0], [803, 99.0], [876, 82.0], [949, 100.0], [1022, 102.0], [1095, 92.0]],
                          (14, 2): [[730, 280.0], [803, 21.0], [876, 26.0], [949, 28.0], [1022, 13.0], [1095, 24.0]]}
                         )
        self.assertEqual(output_parser.survey_output_data[(3, 2)],
                         [[730, 16.0], [803, 17.0], [876, 16.0], [949, 14.0], [1022, 12.0], [1095, 10.0]])

    def test_vector_measures(self):
        output_parser = OutputParser(open(os.path.join(base_dir, "test1.xml")),
                                     survey_output_file=open(os.path.join(base_dir, "test1_output.txt")),
                                     cts_output_file=open(os.path.join(base_dir, "test1_ctsout.txt")))
        self.assertEqual(len(output_parser.cts_output_data["N_v0(arabiensis)"]), 1461)
        self.assertEqual(output_parser.get_cts_measures(),
                         ['input EIR',
                          'simulated EIR',
                          'human infectiousness',
                          'N_v0(gambiae)',
                          'N_v0(arabiensis)',
                          'N_v0(funestus)',
                          'N_v0(minor)',
                          'immunity h',
                          'immunity Y',
                          'new infections',
                          'num transmitting humans',
                          'ITN coverage',
                          'IRS coverage',
                          'GVI coverage',
                          'alpha_i(gambiae)',
                          'alpha_i(arabiensis)',
                          'alpha_i(funestus)',
                          'alpha_i(minor)',
                          'P_B(gambiae)',
                          'P_B(arabiensis)',
                          'P_B(funestus)',
                          'P_B(minor)',
                          'P_C*P_D(gambiae)',
                          'P_C*P_D(arabiensis)',
                          'P_C*P_D(funestus)',
                          'P_C*P_D(minor)']
                         )
        self.assertEqual(len(output_parser.survey_time_list), 241)
        self.assertEqual(len(output_parser.survey_output_data[(34, "funestus")]), 241)

        # Measure 21, allCauseIMR is returned as a single number over whole intervention period
        self.assertEqual(output_parser.survey_output_data[(21, 1)], [[0, 152.089]])

    def test_nan(self):
        output_parser = OutputParser(open(os.path.join(base_dir, "scenario_nan.xml")),
                                     survey_output_file=open(os.path.join(base_dir, "output_nan.txt")),
                                     cts_output_file=open(os.path.join(base_dir, "ctsout_nan.txt")))
        # allCauseIMR measure (#21) can produce NaN value on timestep 0
        allCauseIMR = output_parser.survey_output_data[(21, 1)]
        # Expected value [[0, float('NaN')]]
        # Note you can't do self.assertEqual(test_output_parser.survey_output_data[(21, 1)], [[0, float('NaN')]])
        # because float('NaN') != float('NaN')
        self.assertEqual(len(allCauseIMR), 1)
        self.assertEqual(len(allCauseIMR[0]), 2)
        self.assertTrue(math.isnan(allCauseIMR[0][1]))

    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()
